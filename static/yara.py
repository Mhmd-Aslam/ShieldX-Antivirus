import yara
import os

class YaraScanner:
    def __init__(self):
        rule_paths = {}
        for directory in os.listdir("./vendor/reversinglabs/yara"):
            for path in os.listdir(f"./vendor/reversinglabs/yara/{directory}"):
                rule_paths[path] = f"./vendor/reversinglabs/yara/{directory}/{path}"

        print(rule_paths)
        
        self.compiled_rules = yara.compile(filepaths=rule_paths)

    def scan(self, path):
        with open(path, "rb") as file:
            return self.compiled_rules.match(data=file.read())