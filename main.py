from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI(title="Miko API")


@app.get("/")
def home():
    return {"message": "Miko API is running"}


@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Keep only the basename so a client cannot write outside the working directory.
    safe_name = Path(file.filename or "resume").name
    if not safe_name or safe_name in {".", ".."}:
        raise HTTPException(status_code=400, detail="A valid resume filename is required")

    payload = await file.read()
    if not payload:
        raise HTTPException(status_code=400, detail="Uploaded resume is empty")

    resume_path = f"temp_{safe_name}"
    with open(resume_path, "wb") as output:
        output.write(payload)

    return {
        "filename": safe_name,
        "path": resume_path,
        "message": "Resume received and saved",
    }
