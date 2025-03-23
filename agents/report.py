from static.metadata import StaticAnalyzer, ELFAnalyzer, PEAnalyzer
from dynamic.virustotal import Client

class ReportGenerator:
  def __init__(self, path):
    self.path = path
    self.staticAnalyzer = StaticAnalyzer(path)
    self.type = ""
    self.static_report = None
    self.dynamic_report = None
    self.hashes = self.staticAnalyzer.hashes
    self.scannable = True

    print(self.staticAnalyzer.file_type)
    
    if self.staticAnalyzer.file_type:
      if "exe" in self.staticAnalyzer.file_type:
        self.binaryAnalyzer = PEAnalyzer(path)
        self.type = "pe"
      elif "elf" in self.staticAnalyzer.file_type:
        self.binaryAnalyzer = ELFAnalyzer(path)
        self.type = "elf"
      else:
        self.scannable = False
    else:
      self.scannable = False

  def generate_static_report(self):
    """
    Generate a static report using the appropriate analyzer.
    
    :return: Dictionary containing static analysis information.
    """
    if self.static_report:
      return self.static_report

    sections = []
    if not self.binaryAnalyzer:
      return None

    for section in self.binaryAnalyzer.sections:
      match self.type:
        case "pe":
          sections.append({
            "name": section.Name.decode("utf-8", errors="ignore").rstrip("\x00"),
            "size_of_raw_data": section.SizeOfRawData,
            "number_of_relocations": section.NumberOfRelocations,
            "virtual_address": section.VirtualAddress,
            "entropy": section.get_entropy()
          })
        case "elf":
          sections.append({
            "name": section.name,
            "size": section["sh_size"],
            "address": section["sh_addr"],
            "type": section["sh_type"]
          })
    import_symbols = []
    if self.type == "pe":
      import_symbols = [{
        "dll": entry.dll.decode("utf-8", errors="ignore"),
        "imports": [{
          "name": imp.name.decode("utf-8", errors="ignore") if imp.name else None,
          "address": hex(imp.address)
        } for imp in entry.imports]
      } for entry in self.binaryAnalyzer.import_symbols]


    self.static_report = {
      "file_type": self.staticAnalyzer.file_type,
      "sections": sections,
      "import_symbols": import_symbols
    }

    return self.static_report

  def generate_dynamic_report(self):
    """
    Generate a dynamic report using the VirusTotal client.
    
    :return: Dictionary containing dynamic analysis information.
    """
    if self.dynamic_report:
      return self.dynamic_report
    
    if not self.binaryAnalyzer:
      return None

    client = Client(self.path)
    behaviour_reports = client.behaviour_reports()["data"]["attributes"]
    mitre_tactics = client.mitre_tactics()["data"]["Zenbox"]

    self.dynamic_report = {
      "behaviour_reports": behaviour_reports,
      "attack_tactics": mitre_tactics
    }

    return self.dynamic_report