from agents.summarizer import summarize_analysis
from agents.report import ReportGenerator

def main():
    # Path to the binary file to be analyzed
    binary_path = "tests/assets/satan.exe"

    # Generate reports
    report_generator = ReportGenerator(binary_path)
    static_report = report_generator.generate_static_report()
    dynamic_report = report_generator.generate_dynamic_report()

    # Summarize analysis
    summarize_analysis(static_report, dynamic_report["behaviour_reports"])

if __name__ == "__main__":
    main()

