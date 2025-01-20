import pefile
import peutils
import magic
from datetime import datetime
from capstone import *

class StaticAnalyzer:
    """Base class for all static analysis tasks"""
    def __init__(self, path):
        """
        Initialize the StaticAnalyzer with the path to the file to be analyzed.
        
        :param path: Path to the file to be analyzed.
        """
        self.path = path

    def get_strings(self):
        """
        Extract all strings from the file.
        
        :return: Decoded strings from the file.
        """
        with open(self.path, "rb") as file:
            return file.read().decode("utf-8", errors="ignore")
        
    def file_type(path):
        """
        Get the file type using the magic library.
        
        :param path: Path to the file.
        :return: File type as a string.
        """
        return magic.from_file(path)
    
    def file_type(self):
        """
        Get the file type using the magic library.
        
        :return: File type as a string.
        """
        return magic.from_file(self.path)

class PEAnalyzer(StaticAnalyzer):
    """Analyzer class for Windows executables"""
    def __init__(self, path):
        """
        Initialize the PEAnalyzer with the path to the PE file.
        
        :param path: Path to the PE file.
        """
        super().__init__(path)
        self.executable = pefile.PE(path) # Avoid wasting time on directories

    def __str__(self):
        """
        Return a string representation of the PE file information.
        
        :return: String representation of the PE file information.
        """
        return self.executable.dump_info()
    
    def info(self):
        """
        Get detailed information about the PE file.
        
        :return: Dictionary containing PE file information.
        """
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
        """
        Disassemble the specified section of the PE file.
        
        :param section: Section of the PE file to disassemble.
        :return: List of disassembled instructions.
        """
        image_base = self.executable.OPTIONAL_HEADER.ImageBase
                
        data = self.executable.get_memory_mapped_image()
        
        start_offset = section.VirtualAddress
        code_size = section.SizeOfRawData
        
        # Initialize disassembler for x64
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        md.skipdata = True
        
        # Disassemble the entire code section
        code_bytes = data[start_offset:start_offset + code_size]
        
        instructions = []
        for inst in md.disasm(code_bytes, start_offset+image_base):
            instructions.append({
                "address": inst.address,
                "mnemonic": inst.mnemonic,
                "bytes": inst.bytes,
                "arguments": inst.op_str
            })

        return instructions