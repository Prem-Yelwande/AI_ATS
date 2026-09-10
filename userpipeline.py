from agents import Resume_Extractor, Validator_chain
from database import get_session, save_resume


def process_resume(resume_path, user_id):

    print("\n" + "=" * 50)
    print("step 1 Extractor agent working")
    print("=" * 50)

    agent = Resume_Extractor()

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"Parse the resume from this file: {resume_path}"
            }
        ]
    })

    resume = result["structured_response"]

    print(resume)

    print("\n" + "=" * 50)
    print("step 2 Validator chain working")
    print("=" * 50)

    validator = Validator_chain()

    result = validator.invoke({
        "resume": resume
    })

    print(result)

    if result.is_valid:

        session = get_session()

        resume_record = save_resume(
            session=session,
            user_id=user_id,
            resume_data=resume,
            source="uploaded"
        )

        print("\nResume saved successfully!")
        print("Resume ID:", resume_record.id)
        print("User ID:", resume_record.user_id)
        print("Version:", resume_record.version)

        return resume_record

    else:
        print("\nResume validation failed!")
        return None