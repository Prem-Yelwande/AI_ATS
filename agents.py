from tools import *
from states import *
from prompts import *
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.globals import set_verbose, set_debug
from langgraph.graph import StateGraph
from langgraph.constants import END
from dotenv import load_dotenv
import os
from langchain_mistralai import ChatMistralAI

load_dotenv()

# Primary model for structured extraction (reliable structured output)
llm1 = ChatMistralAI(
    model = "mistral-small-latest",
    api_key=os.getenv("MISTRAL_AI_API"),
    temperature=0
)

# Fast alternative via Groq
llm2 = ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key = os.getenv("GROQ_API_KEY"),
    temperature=0
)
 
# Guardrail / safety model
llm3 = ChatNVIDIA(
    model="llama-guard-4-12b",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0
)
 
# Default model used by agents (good balance of quality and speed)
llm4 = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    api_key=os.getenv("GOOGLE_API_KEY")
)


def Resume_Extractor():
    """Agent that extracts structured data from a resume using the available tools."""
    return create_agent(
        model=llm4,
        tools=[
                    file_type_detector,
                    pdf_extractor,
                    docx_extractor
                ],
        system_prompt= ResumeExtractor(),
        response_format=ResumeData
    )

def Validator_chain():
    """Chain that validates extracted resume data against the target role."""
    validator_chain = validator_prompt | llm4.with_structured_output(ResumeValidation)
    return validator_chain
