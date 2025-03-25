import os
import platform
from typing import List

def get_removable_drives() -> List[str]:
    """Get list of removable drives on the system"""
    drives = []
    
    if platform.system() == "Windows":
        import win32api
        import win32file
        drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
        drives = [d for d in drives if win32file.GetDriveType(d) == win32file.DRIVE_REMOVABLE]
    
    elif platform.system() == "Linux":
        # Check common mount points for removable media
        mounts = []
        with open('/proc/mounts', 'r') as f:
            mounts = f.readlines()
        
        common_removable = ['/media/', '/mnt/', '/run/media/']
        drives = [m.split()[1] for m in mounts if any(m.startswith(prefix) for prefix in common_removable)]
    
    elif platform.system() == "Darwin":  # macOS
        # Check /Volumes for mounted drives
        if os.path.exists('/Volumes'):
            drives = [os.path.join('/Volumes', d) for d in os.listdir('/Volumes') 
                     if os.path.ismount(os.path.join('/Volumes', d))]
    
    # Filter out non-existent drives and return
    return [d for d in drives if os.path.exists(d)]