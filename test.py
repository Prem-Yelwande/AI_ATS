
from agents import Resume_Extractor, Validator_chain
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

    print(state["resume"])

    print("\n" + "=" * 50)
    print("step 2 Validator chain working")
    print("=" * 50)

    validator = Validator_chain()

    result = validator.invoke({
    "resume": state["resume"]
})

    print(result)

if __name__ == "__main__":
    main()

    

