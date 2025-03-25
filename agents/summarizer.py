from langchain_groq.chat_models import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from typing import List
from agents.reasoner import filter_useful_reg_keys, filter_useful_calls, filter_useful_files
import os

load_dotenv()

llama = ChatGroq(
  model="llama3-70b-8192",
  api_key=os.environ["GROQ_API_KEY"]
)

def format_prompt_content(tags, techniques, urls, calls, symbols):
    """Format the content for the human prompt."""
    return f"""
        TAGS:
        {tags}
        MITRE_ATTACK_TECHNIQUES:
        {techniques}
        MEMORY_PATTERN_URLS:
        {urls}
        API_CALLS:
        {calls}
        IMPORT_SYMBOLS:
        {symbols}
    """

def naive_chunk_text(text, max_length=5000):
    """
    A simple chunker that splits text into chunks of maximum length.
    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    
    # Process text in max_length chunks
    for i in range(0, len(text), max_length):
        chunk = text[i:i + max_length]
        chunks.append(chunk)
    
    return chunks

def summarizer_agent(report: dict, static: dict, max_chunk_size=5000):
  # Handle potentially missing keys with default empty values
  tags = ",".join(report.get("tags", []) or [])
  
  mitre_attack_techniques = ""
  if "mitre_attack_techniques" in report and report["mitre_attack_techniques"]:
    for technique in report["mitre_attack_techniques"]:
      if isinstance(technique, dict):
        signature = technique.get("signature_description", "Unknown")
        severity = technique.get("severity", "Unknown")
        if severity == "Unknown":
          continue
        mitre_attack_techniques += f"{signature} - {severity}; "

  memory_pattern_urls = ",".join(report.get("memory_pattern_urls", []) or [])
  
  # Extract and filter API calls
  api_calls = ""
  if "calls_highlighted" in report and report["calls_highlighted"]:
    api_calls = ",".join(report["calls_highlighted"])
    if len(api_calls) > 2000:
      api_calls = filter_useful_calls(api_calls)
  
  # Get import symbols
  import_symbols = static.get("import_symbols", "")
  
  print("summarizing")
  
  # Format the entire prompt content
  full_prompt_content = format_prompt_content(
    tags, 
    mitre_attack_techniques, 
    memory_pattern_urls, 
    api_calls, 
    import_symbols
  )
  
  # Use the naive chunker with max length of 5000 characters
  prompt_chunks = naive_chunk_text(full_prompt_content, max_chunk_size)
  
  print(f"Chunked prompt into {len(prompt_chunks)} parts")
  
  # If we only have one chunk, process normally
  if len(prompt_chunks) == 1:
    prompt_template = ChatPromptTemplate.from_messages([
      ("system", "You are a summarizing agent responsible for generating a summary of a report. Do not make any judgements on the given information; Present the information as is in a detailed manner. Ensure all the imported dlls, urls, registry keys and any other information is also included."),
      ("human", "{content}")
    ])

    chain = prompt_template | llama
    result = chain.invoke({"content": prompt_chunks[0]}).content

    return result
  
  # If we have multiple chunks, process each and then combine
  summaries = []
  
  for i, chunk in enumerate(prompt_chunks):
    prompt_template = ChatPromptTemplate.from_messages([
      ("system", "You are a summarizing agent responsible for generating a partial summary of a report section. Focus on the information provided in this chunk without making judgements. Keep summaries under 1000 tokens."),
      ("human", """
        {content}
        
        This is chunk {chunk_num} of {total_chunks}. Provide a detailed summary of this section.
      """)
    ])

    chain = prompt_template | llama
    
    result = chain.invoke({
      "content": chunk,
      "chunk_num": i + 1,
      "total_chunks": len(prompt_chunks)
    }).content
    
    summaries.append(result)
  
  # If we have multiple summaries, combine them
  if len(summaries) > 1:
    final_prompt = ChatPromptTemplate.from_messages([
      ("system", "You are a summarizing agent responsible for combining multiple partial summaries into a coherent final summary. Ensure there is no redundancy while preserving all important information."),
      ("human", "Here are {num_summaries} partial summaries from different chunks of the same report. Combine them into a single coherent summary:\n\n{all_summaries}")
    ])
    
    chain = final_prompt | llama
    
    final_result = chain.invoke({
      "num_summaries": len(summaries),
      "all_summaries": "\n\n--- NEXT SUMMARY ---\n\n".join(summaries)
    }).content
    
    with open("summary.txt", "w") as file:
      file.write(final_result)

    return final_result
  
  else:
    with open("summary.txt", "w") as file:
      file.write(summaries[0])
    return summaries[0]