from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

deepseek = ChatGroq(
  model="deepseek-r1-distill-llama-70b",
  api_key=GROQ_API_KEY
)



def reason_malware_report(report: str):
  system_prompt = """
You are a malware analysis agent that is part of a bigger antivirus module. You will be provided with a report containing the results of static and dynamic analysis of a malware sample. Based on the given report, generate a <result> resource.

Format of report:
{"file_type": string, ""}
"""

  prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{report}")
  ])