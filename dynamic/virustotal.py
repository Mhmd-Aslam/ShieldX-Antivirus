from dotenv import load_dotenv
from static.metadata import StaticAnalyzer
import requests
import os

load_dotenv()

class Client:
  def __init__(self, file):
    self.file = file
    self.apiKey = os.getenv("VT_API_KEY")

    with open(self.file, "rb") as f:
      response = requests.post("https://www.virustotal.com/api/v3/files", headers={
        "accept": "application/json",
        "x-apikey": self.apiKey
      }, files={
        "file": file
      })

      staticAnalyzer = StaticAnalyzer(self.file)
      self.hash = staticAnalyzer.hashes

      data = response.json()
      self.analysisId = data["data"]["id"]

  def behaviour_reports(self):
    response = requests.get(f"https://www.virustotal.com/api/v3/file_behaviours/{self.hash["sha256"]}_Zenbox", headers={
      "accept": "application/json",
      "x-apikey": self.apiKey
    })

    return response.json()

  def mitre_tactics(self):
    response = requests.get(f"https://www.virustotal.com/api/v3/files/{self.hash["sha256"]}/behaviour_mitre_trees", headers={
      "accept": "application/json",
      "x-apikey": self.apiKey
    })

    return response.json()