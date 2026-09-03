from extractor import Doc_Extractor
from rich import print

resume_path = r"C:\Users\24101A0079\Desktop\Application Tracking System\dummy_resume.pdf"

def main():
    agent = Doc_Extractor()

    resume_path = "resume.pdf"

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"Parse the resume from this file: {resume_path}"
            }
        ]
    })

    print(result)


if __name__ == "__main__":
    main()