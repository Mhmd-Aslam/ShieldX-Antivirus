from dynamic import virustotal
import json

client = virustotal.Client("tests/assets/CrimsonRAT.exe")
with open("dynamic.json", "w") as file:
  file.write(json.dumps(client.mitre_tactics()))