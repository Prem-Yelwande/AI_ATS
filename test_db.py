from database import get_session, save_resume
from states import ResumeData

session = get_session()

resume_data = ResumeData(
    name="Prem Yelwande",
    email="prem@example.com",
    skills=[
        {
            "skills": {
                "languages": ["Python", "Java"],
                "backend": ["FastAPI"],
                "ai_ml": ["LangChain"]
            }
        }
    ]
)

resume = save_resume(
    session=session,
    user_id=1,
    resume_data=resume_data,
    source="uploaded"
)

print("Resume ID:", resume.id)
print("Version:", resume.version)
print("User ID:", resume.user_id)
print("Source:", resume.source)

session.close()