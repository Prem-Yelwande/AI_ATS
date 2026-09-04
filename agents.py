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

llm1 = ChatMistralAI(
    model = "mistral-small-latest",
    api_key=os.getenv("MISTRAL_AI_API"),
    temperature=0
)

llm2 = ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key = os.getenv("GROQ_API_KEY"),
    temperature=0
)

llm3 = ChatNVIDIA(
    model="nvidia/nemotron-3-super-120b-a12b",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0
)

llm4 = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    api_key=os.getenv("GOOGLE_API_KEY")
)

def Resume_Extractor():
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
