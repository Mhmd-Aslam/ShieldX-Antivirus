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

llama3versatile = ChatGroq(
  model="llama-3.3-70b-versatile",
  api_key=GROQ_API_KEY
)

def chunk_text(text, max_chunk_size=2000):
  """
  Split a comma-separated text into chunks under the specified size.
  Returns a list of chunks.
  """
  if len(text) <= max_chunk_size:
    return [text]
  
  items = text.split(',')
  chunks = []
  current_chunk = []
  current_size = 0
  
  for item in items:
    # Add comma if this isn't the first item in the chunk
    item_size = len(item) + (1 if current_chunk else 0)
    
    if current_size + item_size > max_chunk_size and current_chunk:
      # Current chunk would exceed limit, save it and start a new one
      chunks.append(','.join(current_chunk))
      current_chunk = [item]
      current_size = len(item)
    else:
      # Add to current chunk
      current_chunk.append(item)
      current_size += item_size
  
  # Add the last chunk if not empty
  if current_chunk:
    chunks.append(','.join(current_chunk))
  
  return chunks

def filter_useful_reg_keys(regkeys):
  system_prompt = """
You are a specialized malware analysis assistant focused on identifying and analyzing potentially malicious registry key modifications. Your primary tasks include systematically filtering and categorizing registry keys, identifying suspicious registry key patterns, and providing detailed forensic insights into potential malware indicators. When examining registry keys, prioritize high-risk categories such as persistence mechanisms (autorun locations, Windows Run/RunOnce keys, service registrations), system configuration modifications, and communication network changes. Flag registry keys with characteristics like randomly generated names, modifications in non-standard locations, recent changes to critical system paths, keys with executable references, and unexpected permission modifications. Only output the list of flagged registry keys as a comma separated list.
"""

  if len(regkeys) <= 5000:
    prompt_template = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      ("user", "REGISTRY KEYS: {registry}")
    ])

    chain = prompt_template | llama3versatile
    output = chain.invoke({"registry": regkeys}).content
    return output

  # Process in chunks to avoid token limits
  chunks = chunk_text(regkeys)
  print(f"Registry keys split into {len(chunks)} chunks")
  
  filtered_results = []
  for i, chunk in enumerate(chunks):
    prompt_template = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      ("user", f"REGISTRY KEYS (CHUNK {i+1}/{len(chunks)}): {{registry}}")
    ])

    chain = prompt_template | llama3versatile
    result = chain.invoke({"registry": chunk}).content
    filtered_results.append(result)
  
  combined_result = ','.join(filtered_results)
  return combined_result

def filter_useful_calls(calls):
  system_prompt = """
You are a specialized malware analysis assistant focused on identifying potentially suspicious API calls. When examining a list of API calls, identify those commonly associated with malicious behavior such as process manipulation, encryption, network communication, registry modifications, and evasion techniques. Focus on identifying calls that might indicate suspicious activities while filtering out common benign calls. Only output the filtered list of suspicious API calls as a comma separated list, or return the original list if it's already short.
"""

  if len(calls) <= 5000:
    prompt_template = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      ("user", "API CALLS: {calls}")
    ])

    chain = prompt_template | llama3versatile
    output = chain.invoke({"calls": calls}).content
    return output

  # Process in chunks to avoid token limits
  chunks = chunk_text(calls)
  print(f"API calls split into {len(chunks)} chunks")
  
  filtered_results = []
  for i, chunk in enumerate(chunks):
    prompt_template = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      ("user", f"API CALLS (CHUNK {i+1}/{len(chunks)}): {{calls}}")
    ])

    chain = prompt_template | llama3versatile
    result = chain.invoke({"calls": chunk}).content
    filtered_results.append(result)
  
  combined_result = ','.join(filtered_results)
  return combined_result

def filter_useful_files(files):
  system_prompt = """
You are a specialized malware analysis assistant focused on identifying suspicious files accessed by potential malware. When examining a list of files, identify those that might indicate malicious behavior, such as access to system files, creation of unusual executables, or modifications to startup locations. Focus on identifying file access patterns that might indicate suspicious activities while filtering out common benign file access. Only output the filtered list of suspicious files as a comma separated list, or return the original list if it's already short.
"""

  if len(files) <= 5000:
    prompt_template = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      ("user", "FILES ACCESSED: {files}")
    ])

    chain = prompt_template | llama3versatile
    output = chain.invoke({"files": files}).content
    return output

  # Process in chunks to avoid token limits
  chunks = chunk_text(files)
  print(f"Files accessed split into {len(chunks)} chunks")
  
  filtered_results = []
  for i, chunk in enumerate(chunks):
    prompt_template = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      ("user", f"FILES ACCESSED (CHUNK {i+1}/{len(chunks)}): {{files}}")
    ])

    chain = prompt_template | llama3versatile
    result = chain.invoke({"files": chunk}).content
    filtered_results.append(result)
  
  combined_result = ','.join(filtered_results)
  return combined_result

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
2. Start with a baseline confidence score of 0%
3. Incrementally adjust confidence based on specific evidence:
   - Mitre attack techniques with IMPACT_SEVERITY_INFO are not indicators of malware. Only treat them as indicators of malware if it's obvious that it's an indicator of malware.
   - Each suspicious indicator: +5-10% (depending on severity)
   - Each confirmed malicious behavior: +15-20%
   - Multiple indicators correlating to known malware family: +25%
4. Only classify as malware if confidence exceeds 70% with concrete supporting evidence
5. If you're not sure what the malware family is, make an educated guess.

RESULT FORMAT:
<result>
{{"is_malware": boolean,"confidence": number (0-100),"malware_family": string,"description": string}}
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

  with open("reason.txt", "w") as file:
    file.write(output)

  json_match = re.search(r'<result>\s*(.*?)\s*</result>', output)
  return json.loads(json_match.group(1))