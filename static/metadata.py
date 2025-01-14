import pefile
import peutils
import magic
from datetime import datetime
from capstone import *
from typing import Dict

class StaticAnalyzer:
    """Base class for all static analysis tasks"""
    def __init__(self, path):
        self.path = path

    def get_strings(self):
        with open(self.path, "rb") as file:
            return file.read().decode("utf-8", errors="ignore")
        
    def file_type(path):
        return magic.from_file(path)
    
    def file_type(self):
        return magic.from_file(self.path)

class PEAnalyzer(StaticAnalyzer):
    """Analyzer class for windows executables"""
    def __init__(self, path):
        super().__init__(path)
        self.executable = pefile.PE(path) #Avoid wasting time on directories

    def __str__(self):
        return self.executable.dump_info()
    
    def info(self):
        return {
            "machine_type": self.executable.FILE_HEADER.Machine,
            "timestamp": datetime.fromtimestamp(self.executable.FILE_HEADER.TimeDateStamp).strftime("%d/%m/%Y, %H:%M:%S"),
            "file_type": super().file_type(),
            "packed": peutils.is_probably_packed(self.executable),
            "size_of_code": hex(self.executable.OPTIONAL_HEADER.SizeOfCode),
            "entry_point": hex(self.executable.OPTIONAL_HEADER.AddressOfEntryPoint),
            "image_base": hex(self.executable.OPTIONAL_HEADER.ImageBase)
        }
    
    def disassemble(self, section: pefile.SectionStructure):
        try:
            image_base = self.executable.OPTIONAL_HEADER.ImageBase
                
            data = self.executable.get_memory_mapped_image()
            
            start_offset = section.VirtualAddress
            code_size = section.SizeOfRawData
            
            # Initialize disassembler for x64
            md = Cs(CS_ARCH_X86, CS_MODE_64)
            
            # Disassemble the entire code section
            code_bytes = data[start_offset:start_offset + code_size]
            
            for inst in md.disasm(code_bytes, start_offset+image_base):
                yield {
                    "address": inst.address,
                    "mnemonic": inst.mnemonic,
                    "bytes": inst.bytes,
                    "arguments": inst.op_str
                }
                
        except Exception as e:
            print(f"Disassembly error: {str(e)}")
            return []

    
if __name__ == "__main__":
    pe = PEAnalyzer("tests/malware.exe")
    for section in pe.executable.sections:
        print(section)
        for instruction in pe.disassemble(section):
            print(f"{hex(instruction["address"])}:  {instruction["mnemonic"]} {instruction["arguments"]}")
        print()