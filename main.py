from scanner.scanner import Scanner

def main():
    scan_path = "./tests"
    print(f"Starting scan of {scan_path}")
    
    scanner = Scanner()
    for malware_path in scanner.full_scan(scan_path):
        print(malware_path)
    
if __name__ == "__main__":
    main()

