from agents import Resume_Extractor
from rich import print


def main():
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

    print(resume)


if __name__ == "__main__":
    main()
