from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI(title="Miko API")

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB


@app.get("/")
def home():
    return {"message": "Miko API is running"}


@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Keep only the basename so a client cannot write outside the working directory.
    safe_name = Path(file.filename or "resume").name
    if not safe_name or safe_name in {".", ".."}:
        raise HTTPException(status_code=400, detail="A valid resume filename is required")

    suffix = Path(safe_name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{suffix}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    payload = await file.read()
    if not payload:
        raise HTTPException(status_code=400, detail="Uploaded resume is empty")
    if len(payload) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Resume exceeds the 5 MB size limit")

    resume_path = f"temp_{safe_name}"
    with open(resume_path, "wb") as output:
        output.write(payload)

    return {
        "filename": safe_name,
        "path": resume_path,
        "message": "Resume received and saved",
    }
