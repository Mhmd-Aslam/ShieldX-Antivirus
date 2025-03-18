from dotenv import load_dotenv
from static.metadata import StaticAnalyzer
import requests
import os
import json

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
        "file": f.read()
      })

      data = response.json()
      print(data)

      self.analysisId = data["data"]["id"]

      hash_response = requests.get(f"https://www.virustotal.com/api/v3/analyses/{self.analysisId}", headers={
        "accept": "application/json",
        "x-apikey": self.apiKey
      })

      self.hash = hash_response.json()["meta"]["file_info"]

  def behaviour_reports(self):
    response = requests.get(f"https://www.virustotal.com/api/v3/file_behaviours/{self.hash["sha256"]}_Zenbox", headers={
      "accept": "application/json",
      "x-apikey": self.apiKey
    })

    data = response.json()
    # with open("dynamic.json", "w") as file:
    #   file.write(json.dumps(data))
    return data

  def mitre_tactics(self):
    response = requests.get(f"https://www.virustotal.com/api/v3/files/{self.hash["sha256"]}/behaviour_mitre_trees", headers={
      "accept": "application/json",
      "x-apikey": self.apiKey
    })

    return response.json()