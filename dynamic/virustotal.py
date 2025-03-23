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
      #get upload url
      upload_url_response = requests.get("https://www.virustotal.com/api/v3/files/upload_url", headers={
        "accept": "application/json",
        "x-apikey": self.apiKey
      })

      upload_url_data = upload_url_response.json()

      response = requests.post(upload_url_data["data"], headers={
        "accept": "application/json",
        "x-apikey": self.apiKey
      }, files={
        "file": f.read()
      })

      print(response.text)
      data = response.json()

      self.analysisId = data["data"]["id"]

      hash_response = requests.get(f"https://www.virustotal.com/api/v3/analyses/{self.analysisId}", headers={
        "accept": "application/json",
        "x-apikey": self.apiKey
      })

      self.hash = hash_response.json()["meta"]["file_info"]
      print(self.hash)

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