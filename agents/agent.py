import scipy.spatial
from agents.report import ReportGenerator
from agents.summarizer import summarizer_agent
from agents.reasoner import reason_malware_report
from agents.embedder import generate_embeddings
from db.models import HashDB, VectorDB, ReportCache

class MalwareAgent:
  def __init__(self, path):
    self.path = path
    self.report_generator = ReportGenerator(self.path)
    self.vector_db = VectorDB()
    self.hash_db = HashDB()
    self.cache = ReportCache()
    self.embeddings = None
    self.summary = None

  def check_embeddings(self):
    cached_summary = self.cache.get_cache(self.report_generator.hashes["sha256"])
    if cached_summary:
      print("Using cached response")
      self.summary = cached_summary[0]
    else:
      static_report = self.report_generator.generate_static_report()
      dynamic_report = self.report_generator.generate_dynamic_report()

      self.summary = summarizer_agent(dynamic_report["behaviour_reports"], static_report)
      self.cache.insert_cache(self.report_generator.hashes["sha256"], self.summary)
      print("inserted into cache")

    self.embeddings = generate_embeddings(self.summary)

    closest_matches = self.vector_db.find_closest_match(self.embeddings)
    return closest_matches
    
  def analyze_report(self):
    result = reason_malware_report(self.summary)

    if result['is_malware'] and result['confidence'] > 60:
      self.vector_db.insert_malware_embedding(self.embeddings, self.report_generator.hashes["sha256"])
      self.hash_db.add_malware_hash(self.report_generator.hashes["sha256"], self.path)
    else:
      self.hash_db.add_safe_hash(self.report_generator.hashes["sha256"], self.path)
    
    return result

  def is_malware(self):
    if not self.report_generator.scannable:
      return False

    closest_matches = self.check_embeddings()
    print(closest_matches)
    
    # Properly handle ChromaDB results which come as a dictionary
    # with 'distances' as a list of distance values
    if closest_matches and 'distances' in closest_matches and len(closest_matches['distances']) > 0:
      # Lower distance means higher similarity in cosine similarity
      # Using 0.1 threshold (meaning 90% similarity)
      for distance in closest_matches['distances'][0]:
        if distance < 0.1:  # Cosine distance is low (high similarity)
          return True
    
    reasoned_report = self.analyze_report()
    if reasoned_report['is_malware'] and reasoned_report['confidence'] > 60:
      return True
    
    return False