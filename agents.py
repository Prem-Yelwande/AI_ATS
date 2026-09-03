from tools import *
from states import *
from prompts import *
from langchain.agents import create_agent
from rich import print 
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


