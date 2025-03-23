import sqlite3
import chromadb

class ReportCache:
  def __init__(self):
    self.connection = sqlite3.connect("./db/av.db")
    self.cursor = self.connection.cursor()

  def insert_cache(self, hash: str, summary: str):
    self.cursor.execute("INSERT INTO report_cache(`hash`, `report`) VALUES (?,?);", (hash, summary))
    self.connection.commit()

  def get_cache(self, hash: str):
    result = self.cursor.execute("SELECT report FROM report_cache WHERE `hash` = ?;", (hash,))
    return result.fetchone()

  def __del__(self):
    self.cursor.close()
    self.connection.close()

class HashDB:
  def __init__(self):
    self.connection = sqlite3.connect("./db/av.db")
    self.cursor = self.connection.cursor()

  def find_safe_hash(self, hash: str):
    result = self.cursor.execute("SELECT * FROM safe_hashes WHERE `hash` = ?;", (hash,))
    return result.fetchall()
  
  def find_malware_hash(self, hash: str):
    result = self.cursor.execute("SELECT * FROM malware_hashes WHERE `hash` = ?;", (hash,))
    return result.fetchall()
  
  def add_safe_hash(self, hash: str, path: str):
    self.cursor.execute("INSERT INTO safe_hashes(`path`, `hash`) VALUES (?,?);", (path, hash))
    self.connection.commit()

  def add_malware_hash(self, hash: str, path: str):
    self.cursor.execute("INSERT INTO malware_hashes(`hash`) VALUES (?);", (hash,))
    self.connection.commit()

  def __del__(self):
    self.cursor.close()
    self.connection.close()

class VectorDB:
  def __init__(self):
    # Use ChromaDB persistent client
    self.client = chromadb.PersistentClient(path="./db/embedding_db")
    
    # Get or create collection
    try:
        self.collection = self.client.get_collection(name="malware_vectors")
    except:
        self.collection = self.client.create_collection(
            name="malware_vectors",
            metadata={"hnsw:space": "cosine"}  # Using cosine similarity
        )

  def insert_malware_embedding(self, embedding: list, hash_value: str = ""):
    # Insert with ChromaDB format
    self.collection.add(
        embeddings=[embedding],
        ids=[hash_value if hash_value else str(hash(str(embedding)))],
        metadatas=[{"hash": hash_value}]
    )

  def find_closest_match(self, embedding: list):
    # Query using ChromaDB
    results = self.collection.query(
        query_embeddings=[embedding],
        n_results=5
    )
    
    return results