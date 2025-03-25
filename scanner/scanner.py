import hashlib
import os
import tarfile
import tempfile
import platform
from typing import List
from db.models import HashDB
from static.metadata import StaticAnalyzer
from agents.agent import MalwareAgent

class Directory:
    def __init__(self, path, children=[], parent=None):
        self.path = path
        self.children = children
        self.parent = parent
        self.files = [os.path.join(self.path, file_path) 
                     for file_path in os.listdir(self.path) 
                     if not os.path.isdir(os.path.join(self.path, file_path))]

    def get_directory_hash(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            with tarfile.open(temp_path, "w:gz") as tar:
                tar.add(self.path, arcname=os.path.basename(self.path))
            
            hasher = hashlib.sha256()
            with open(temp_path, 'rb') as archive:
                for chunk in iter(lambda: archive.read(4096), b""):
                    hasher.update(chunk)
                    
            return hasher.hexdigest()
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    @staticmethod
    def generate_directory_tree(path, parent=None):
        current_dir = Directory(path=path, children=[], parent=parent)
        
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                child_dir = Directory.generate_directory_tree(item_path, parent=current_dir)
                current_dir.children.append(child_dir)
        
        return current_dir

class Scanner:
    def __init__(self):
        self.hash_db = HashDB()

    def get_removable_drives(self) -> List[str]:
        drives = []
        
        if platform.system() == "Windows":
            import win32api
            import win32file
            drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
            drives = [d for d in drives if win32file.GetDriveType(d) == win32file.DRIVE_REMOVABLE]
        
        elif platform.system() == "Linux":
            try:
                with open('/proc/mounts', 'r') as f:
                    mounts = f.readlines()
                common_removable = ['/media/', '/mnt/', '/run/media/']
                drives = [m.split()[1] for m in mounts 
                         if any(m.split()[1].startswith(prefix) for prefix in common_removable)]
            except FileNotFoundError:
                pass
        
        elif platform.system() == "Darwin":
            if os.path.exists('/Volumes'):
                drives = [os.path.join('/Volumes', d) for d in os.listdir('/Volumes') 
                         if os.path.ismount(os.path.join('/Volumes', d))]
        
        return [d for d in drives if os.path.exists(d)]

    def quick_scan(self, path):
        if os.path.isfile(path):
            analyzer = StaticAnalyzer(path)
            malware_hash_matches = self.hash_db.find_malware_hash(analyzer.hashes["sha256"])

            if len(malware_hash_matches) > 0:
                yield {
                    "path": path,
                    "malware": True,
                    "type": "Known malware (hash match)"
                }
            else:
                yield {
                    "path": path,
                    "malware": False,
                    "type": "Clean"
                }
        elif os.path.isdir(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                yield from self.quick_scan(item_path)

    def full_scan(self, path):
        if os.path.isfile(path):
            analyzer = StaticAnalyzer(path)
            safe_hash_matches = self.hash_db.find_safe_hash(analyzer.hashes["sha256"])
            malware_hash_matches = self.hash_db.find_malware_hash(analyzer.hashes["sha256"])

            if len(safe_hash_matches) > 0:
                yield {
                    "path": path,
                    "malware": False,
                    "type": "Known safe (hash match)"
                }
                return

            if len(malware_hash_matches) > 0:
                yield {
                    "path": path,
                    "malware": True,
                    "type": "Known malware (hash match)"
                }
            else:
                agent = MalwareAgent(path)
                if agent.is_malware():
                    yield {
                        "path": path,
                        "malware": True,
                        "type": "Suspicious behavior"
                    }
                else:
                    yield {
                        "path": path,
                        "malware": False,
                        "type": "Clean"
                    }
        elif os.path.isdir(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                yield from self.full_scan(item_path)

    def removable_scan(self, path):
        # Check for suspicious files
        suspicious_files = ['autorun.inf', 'desktop.ini', 'thumbs.db']
        if os.path.isdir(path):
            for suspicious in suspicious_files:
                file_path = os.path.join(path, suspicious)
                if os.path.exists(file_path):
                    yield {
                        "path": file_path,
                        "malware": True,
                        "type": "Suspicious system file"
                    }

        # Quick scan
        yield from self.quick_scan(path)
        
        # Deep scan of executables
        executable_extensions = ('.exe', '.dll', '.bat', '.cmd', '.vbs', '.js')
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(executable_extensions):
                    file_path = os.path.join(root, file)
                    yield from self.full_scan(file_path)