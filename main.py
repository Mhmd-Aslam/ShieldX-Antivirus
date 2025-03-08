from agents.summarizer import summarizer_agent
from agents.reasoner import reason_malware_report
from agents.report import ReportGenerator

def main():
    # Path to the binary file to be analyzed
    binary_path = "tests/assets/DanaBot.exe"

    # Generate reports
    report_generator = ReportGenerator(binary_path)
    static_report = report_generator.generate_static_report()
    dynamic_report = report_generator.generate_dynamic_report()

    # Summarize analysis
    print(reason_malware_report(summarizer_agent(dynamic_report["behaviour_reports"], static_report)))

if __name__ == "__main__":
    main()

