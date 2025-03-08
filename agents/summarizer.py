from langchain_groq.chat_models import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()

mixtral = ChatGroq(
  model="llama3-70b-8192",
  api_key=os.environ["GROQ_API_KEY"]
)

def summarizer_agent(report: dict, static: dict):
  # Handle potentially missing keys with default empty values
  tags = ",".join(report.get("tags", []) or [])
  
  mitre_attack_techniques = ""
  if "mitre_attack_techniques" in report and report["mitre_attack_techniques"]:
    for technique in report["mitre_attack_techniques"]:
      if isinstance(technique, dict):
        signature = technique.get("signature_description", "Unknown")
        severity = technique.get("severity", "Unknown")
        mitre_attack_techniques += f"{signature} - {severity}; "

  memory_pattern_urls = ",".join(report.get("memory_pattern_urls", []) or [])
  
  registry_keys = ""
  if "registry_keys_set" in report and report["registry_keys_set"]:
    print(report["registry_keys_set"])
    registry_keys = ",".join([item.get('key', '') for item in report["registry_keys_set"] if isinstance(item, dict) and 'key' in item])

  prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a summarizing agent responsible for generating a summary of a report. Do not make any judgements on the given information; Present the information as is in a detailed manner. Ensure all the imported dlls, urls, registry keys and any other information is also included."),
    ("human", """
      TAGS:
      {tags}
      MITRE_ATTACK_TECHNIQUES:
      {techniques}
      MEMORY_PATTERN_URLS:
      {urls}
      REGISTRY_KEYS_SET:
      {registry}
      IMPORT_SYMBOLS:
      {symbols}
    """)
  ])

  print("summarizing")

  chain = prompt_template | mixtral

  result = chain.invoke({
    "tags": tags,
    "techniques": mitre_attack_techniques,
    "urls": memory_pattern_urls,
    "registry": registry_keys,
    "symbols": static["import_symbols"]
  }).content

  print(result)
  return result