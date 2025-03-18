import hashlib
import os
import tarfile
import tempfile
from db.models import HashDB
from static.metadata import StaticAnalyzer
from agents.agent import MalwareAgent

class Directory:
  def __init__(self, path, children=[], parent = None):
    self.path = path
    self.children = children
    self.parent = parent

    self.files = [os.path.join(self.path, file_path) for file_path in os.listdir(self.path) if not os.path.isdir(os.path.join(self.path, file_path))]

  def get_directory_hash(self):
    """
    Calculate a hash for the directory by compressing it and hashing the archive.
    
    Returns:
        str: The hexadecimal hash value of the directory
    """
    # Create a temporary file for the archive
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        # Create a tar archive of the directory
        with tarfile.open(temp_path, "w:gz") as tar:
            tar.add(self.path, arcname=os.path.basename(self.path))
        
        # Calculate hash of the archive file
        hasher = hashlib.sha256()
        with open(temp_path, 'rb') as archive:
            # Read in chunks to handle large files efficiently
            for chunk in iter(lambda: archive.read(4096), b""):
                hasher.update(chunk)
                
        return hasher.hexdigest()
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

  @staticmethod
  def generate_directory_tree(path, parent=None):
    # Create the Directory object for this path
    current_dir = Directory(path=path, children=[], parent=parent)
    
    # Find all subdirectories
    for item in os.listdir(path):
      item_path = os.path.join(path, item)
      if os.path.isdir(item_path):
        # Recursively build the directory tree for this subdirectory
        child_dir = Directory.generate_directory_tree(item_path, parent=current_dir)
        current_dir.children.append(child_dir)
    
    return current_dir

class Scanner:
  def __init__(self):
    self.hash_db = HashDB()

  def quick_scan(self, root: Directory):
    # Scan files in the current directory
    for file_path in root.files:
      analyzer = StaticAnalyzer(file_path)
      malware_hash_matches = self.hash_db.find_malware_hash(analyzer.hashes["sha256"])

      if len(malware_hash_matches) > 0:
        yield {
          "path": file_path
        }

    # Recursively scan all child directories
    for child_dir in root.children:
      yield from self.quick_scan(child_dir)

  def full_scan(self, root: Directory):
    for file_path in root.files:
      analyzer = StaticAnalyzer(file_path)
      safe_hash_matches = self.hash_db.find_safe_hash(analyzer.hashes["sha256"])
      malware_hash_matches = self.hash_db.find_malware_hash(analyzer.hashes["sha256"])

      print(f"Scanning ${file_path}")

      if len(safe_hash_matches) > 0:
        print("Safe hash found")
        continue

      if len(malware_hash_matches) > 0:
        print("Malware hash found")
        yield {
          "path": file_path
        }
      else:
        agent = MalwareAgent(file_path)
        if agent.is_malware():
          yield {
            "path": file_path
          }

    for child_dir in root.children:
      yield from self.full_scan(child_dir)
