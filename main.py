from static.metadata import PEAnalyzer
import json

def generate_report(analyzer):
    report = {
        "file_type": analyzer.file_type,
        "hashes": analyzer.hashes,
        "info": analyzer.info(),
        "sections": [{"name": section.Name.decode().strip(), "size": section.SizeOfRawData} for section in analyzer.sections],
        "import_symbols": [{"dll": entry.dll.decode(), "imports": [str(imp.name) for imp in entry.imports]} for entry in analyzer.import_symbols],
    }
    return report

if __name__ == "__main__":
    analyzer = PEAnalyzer("./tests/assets/CoronaVirus.exe")
    report = generate_report(analyzer)
    
    with open("report.json", "w") as report_file:
        json.dump(report, report_file, indent=4)

    print("Report generated and saved to report.json")