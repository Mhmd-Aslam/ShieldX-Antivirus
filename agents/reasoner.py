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

RULES FOR CONFIDENCE SCORES AND VERDICTS
1. Do not label an executable as malware without proper reasoning for it. Only label an executable as malware if you're more than 60% sure it's malware.
2. Start off with a low confidence score and add more confidence as you find more indicators of malicious behaviour.

RESULT FORMAT
<result>
{{"is_malware": boolean, "confidence": number (0 to 100)}}
</result>
"""

  prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "REPORT: {report}")
  ])

  chain = prompt_template | deepseek

  return chain.invoke({
    "report": report
  }).content