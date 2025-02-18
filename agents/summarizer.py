from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import json

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llama3 = ChatGroq(
  model="llama-3.3-70b-versatile",
  api_key=GROQ_API_KEY
)

def summarize_analysis(static_analysis: dict, dynamic_analysis: dict):
  system = """
You are a summarizing agent that is used as a part of a larger antivirus system. You will be given json representing the output of static and dynamic analysis stages of the malware analysis. generate a summary of the report without omitting any detail.
"""

  prompt_template = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", """
     Static Analysis:
     {static}
     Dynamic Analysis:
     {dynamic}""")
  ])

  prompt = prompt_template.invoke({
    "static": json.dumps(static_analysis),
    "dynamic": json.dumps({
      "tags": dynamic_analysis["tags"],
      "verdicts": dynamic_analysis["verdicts"],
      # "signature_matches": dynamic_analysis["signature_matches"]
    })
  })

  response = llama3.invoke(prompt)
  print(response.content)