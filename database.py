from sqlmodel import SQLModel, create_engine, Session, select
from db_models import User, Resume

DATABASE_URL = "sqlite:///miko.db"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

def get_next_resume_version(session, user_id: int) -> int:
    statement = select(Resume).where(Resume.user_id == user_id)
    resumes = session.exec(statement).all()

    # Skip rows with a missing version so max() does not fail on None.
    versions = [resume.version for resume in resumes if resume.version is not None]
    if not versions:
        return 1

    return max(versions) + 1

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
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(resume)

    return resume
