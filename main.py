from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI(title="Miko API", description="AI-powered Application Tracking System (ATS) for resume analysis")

# Supported resume formats for ATS processing.
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB limit to prevent large file abuse


def _human_size(num_bytes: int) -> str:
    """Return a human-readable size string."""
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KB"
    return f"{num_bytes / (1024 * 1024):.2f} MB"


@app.get("/")
def home() -> Dict[str, str]:
    """Health-check endpoint confirming the API is up."""
    return {
        "message": "Miko API is running",
        "status": "ok",
        "docs": "/docs",
        "upload_endpoint": "/resume/upload",
    }


@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Accept a resume file, validate type and size, then save it temporarily.

    Allowed formats: .pdf, .docx, .doc. Maximum size: 5 MB.
    The file is stored with a temp_ prefix for later processing.
    Note: content-type is not strictly enforced here; extension + size checks provide the primary validation.
    """
    # Keep only the basename so a client cannot write outside the working directory.
    safe_name = Path(file.filename or "resume").name
    if not safe_name or safe_name in {".", ".."}:
        raise HTTPException(status_code=400, detail="A valid resume filename is required")

    suffix = Path(safe_name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type '{suffix}'. "
                f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}. "
                "Please upload a PDF or Word document."
            ),
        )

    payload = await file.read()
    if not payload:
        raise HTTPException(
            status_code=400,
            detail="Uploaded resume is empty. Please select a non-empty file.",
        )
    if len(payload) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=(
                f"Resume exceeds the 5 MB size limit "
                f"(received {_human_size(len(payload))}). "
                "Please compress or use a smaller file."
            ),
        )

    # Temporary file is saved with a temp_ prefix; clean up after processing in production.
    # In production, prefer a proper temp directory (e.g. tempfile.NamedTemporaryFile) and background cleanup.
    resume_path = f"temp_{safe_name}"
    with open(resume_path, "wb") as output:
        output.write(payload)

    return {
        "filename": safe_name,
        "path": resume_path,
        "size_bytes": len(payload),
        "size_human": _human_size(len(payload)),
        "message": "Resume received and saved",
    }
