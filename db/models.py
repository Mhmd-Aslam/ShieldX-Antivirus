import sqlite3
from pymilvus import MilvusClient, DataType

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
    # Use local file for storage instead of server connection
    self.client = MilvusClient(uri="./db/embeddings.db")

    # Check if collection exists, if not create it with proper schema
    if not self.client.has_collection(collection_name="malware_vectors"):
      # Define schema with primary key and vector field
      schema = self.client.create_schema()

      schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
      schema.add_field(field_name="hash", datatype=DataType.VARCHAR, max_length=100)
      schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=768)

      index_params = self.client.prepare_index_params()
      index_params.add_index(
        field_name="embedding",
        index_type="AUTOINDEX",
        metric_type="COSINE"
      )

      # Create collection with specified metric type
      self.client.create_collection(
        collection_name="malware_vectors",
        schema=schema,
        index_params=index_params
      )

  def insert_malware_embedding(self, embedding: list, hash_value: str = ""):
    # Insert with proper data structure (embedding needs to be in a field)
    data = {
      "hash": hash_value,
      "embedding": embedding
    }
    self.client.insert(
      collection_name="malware_vectors",
      data=data
    )

  def find_closest_match(self, embedding: list):
    # Properly formatted search query with parameters
    res = self.client.search(
      collection_name="malware_vectors",
      data=[embedding],
      anns_field="embedding",
      search_params={"metric_type": "COSINE", "params": {"nprobe": 10}},
      limit=5,
      output_fields=["hash", "embedding"]
    )

    return res
  
  def close(self):
    self.client.close()