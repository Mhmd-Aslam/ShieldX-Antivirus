import os
import hashlib
from static.hash_checker import HashChecker

class Scanner:
    def __init__(self):
        self.hash_checker = HashChecker()

    def scan(self, path):
        """
        Scans the given file or directory, calculates hashes, and checks against the malware database.
        """
        infected_files = []

        if os.path.isfile(path):
            # If scanning a single file
            if self._check_file(path):
                infected_files.append(path)
        elif os.path.isdir(path):
            # If scanning a directory
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if self._check_file(file_path):
                        infected_files.append(file_path)

        return infected_files  # Return a list of infected files

    def _check_file(self, file_path):
        """
        Computes the file's SHA256 hash and checks if it's in the malware database.
        """
        file_hash = self._calculate_sha256(file_path)
        return self.hash_checker.is_malicious(file_hash)

    def _calculate_sha256(self, file_path):
        """
        Computes SHA256 hash of a file.
        """
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
