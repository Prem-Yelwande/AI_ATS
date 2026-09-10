from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="Miko API")


@app.get("/")
def home():
    return {"message": "Miko API is running"}

@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):

    resume_path = f"temp_{file.filename}"

    with open(resume_path, "wb") as f:
        f.write(await file.read())

    return {
        "filename": file.filename,
        "path": resume_path,
        "message": "Resume received and saved"
    }