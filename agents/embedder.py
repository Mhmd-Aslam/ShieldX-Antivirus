from langchain_ollama.embeddings import OllamaEmbeddings

nomic_embed_text = OllamaEmbeddings(model="nomic-embed-text:latest")

def generate_embeddings(report: str):
  return nomic_embed_text.embed_query(report)