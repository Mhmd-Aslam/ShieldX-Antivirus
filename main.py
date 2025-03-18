from scanner.scanner import Scanner, Directory


def main():
    root = Directory.generate_directory_tree("./tests")
    
    scanner = Scanner()
    for malware_path in scanner.full_scan(root):
        print(malware_path)
    
if __name__ == "__main__":
    main()

