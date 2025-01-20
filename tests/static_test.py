import unittest
from static import metadata

class TestStatic(unittest.TestCase):
    def test_disassembly_windows(self):
        analyzer = metadata.PEAnalyzer("tests/assets/hello.exe")
        text_section = analyzer.executable.sections[0]

        self.assertTrue(b'.text' in text_section.Name)
        
        instructions = analyzer.disassemble(text_section)
        self.assertTrue(len(instructions) > 0)
        self.assertTrue(instructions[0]["address"] == 0x140001000)
        self.assertTrue(instructions[-1]["address"] == 0x140002bff)