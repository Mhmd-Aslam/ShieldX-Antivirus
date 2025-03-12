from agents.agent import MalwareAgent
import time

def main():
    # Path to the binary file to be analyzed
    binary_path = "tests/assets/DanaBot.exe"
    malware_analyzer = MalwareAgent(binary_path)

    print(malware_analyzer.is_malware())
    malware_analyzer.die()
    time.sleep(0.1)

if __name__ == "__main__":
    main()

