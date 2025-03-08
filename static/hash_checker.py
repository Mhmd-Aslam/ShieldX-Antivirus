class HashChecker:
    def __init__(self):
        # Example: Add some known malicious file hashes (replace with a real database)
        self.malware_hashes = {
            "44d88612fea8a8f36de82e1278abb02f",  # Example hash (MD5 of EICAR test file)
            "6bf55f6b9221b2ec61c889b9f9f46ab1cf029effdd30d3f8d7174bfb38f99d1c",  # SHA256 example
        }

    def is_malicious(self, file_hash):
        """
        Checks if a given file hash exists in the malware database.
        """
        return file_hash in self.malware_hashes
