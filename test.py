
from agents import Resume_Extractor
from rich import print
from database import get_session, save_resume


def main():
    print("\n" + "=" * 50)
    print("step 1 Extractor agent working")
    print("=" * 50)

    agent = Resume_Extractor()

    # Note: Update this path to your local dummy_resume.pdf location
    resume_path = r"C:\Users\Prem\Desktop\AI_ATS\dummy_resume.pdf"

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"Parse the resume from this file: {resume_path}"
            }
        ]
    })

    resume = result["structured_response"]

    state = {}
    state["resume"] = resume

    session = get_session()

    saved_resume = save_resume(
        session=session,
        user_id=1,
        resume_data=state["resume"],
        source="uploaded"
    )

    print("Saved Resume ID:", saved_resume.id)
    print("Saved Version:", saved_resume.version)

    session.close()

    print(state["resume"])


if __name__ == "__main__":
    main()

    

