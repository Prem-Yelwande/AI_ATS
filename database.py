from sqlmodel import SQLModel, create_engine, Session, select
from db_models import User, Resume

DATABASE_URL = "sqlite:///miko.db"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

def get_next_resume_version(session, user_id: int):
    statement = select(Resume).where(Resume.user_id == user_id)
    resumes = session.exec(statement).all()

    if not resumes:
        return 1

    highest_version = max(resume.version for resume in resumes)

    return highest_version + 1

def save_resume(session, user_id: int, resume_data, source: str, job_id: int | None = None):
    version = get_next_resume_version(session, user_id)

    resume = Resume(
        user_id=user_id,
        version=version,
        resume_data=resume_data.model_dump_json(),
        source=source,
        job_id=job_id
    )

    session.add(resume)
    session.commit()
    session.refresh(resume)

    return resume