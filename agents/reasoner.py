from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import re
import json

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

deepseek = ChatGroq(
  model="deepseek-r1-distill-llama-70b",
  api_key=GROQ_API_KEY
)

def reason_malware_report(report: str):
  system_prompt = """
You are a specialized malware analysis agent integrated within an enterprise-grade antivirus system. Your role is to evaluate reports containing both static and dynamic analysis results of potential malware samples, and deliver precise classification verdicts.

When analyzing a submitted report, follow these guidelines:

ANALYSIS METHODOLOGY:
1. First examine static analysis indicators (file properties, signatures, entropy, etc.)
2. Then review dynamic analysis data (network activity, registry changes, process behavior, etc.)
3. Correlate both analysis types to identify patterns consistent with known malware families
4. Apply threat intelligence context to your findings

CLASSIFICATION RULES:
1. Maintain a conservative approach - begin with a presumption of legitimacy
2. Start with a baseline confidence score of 20%
3. Incrementally adjust confidence based on specific evidence:
   - Each suspicious indicator: +5-10% (depending on severity)
   - Each confirmed malicious behavior: +15-20%
   - Multiple indicators correlating to known malware family: +25%
4. Only classify as malware if confidence exceeds 70% with concrete supporting evidence

RESULT FORMAT:
<result>
{{"is_malware": boolean,"confidence": number (0-100),"malware_family": string}}
</result>
"""

  prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "REPORT: {report}")
  ])

  chain = prompt_template | deepseek

  output = chain.invoke({
    "report": report
  }).content

  json_match = re.search(r'<result>\s*(.*?)\s*</result>', output)
  return json.loads(json_match.group(1))