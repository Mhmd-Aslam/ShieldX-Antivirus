import unittest
from static import metadata

class TestStatic(unittest.TestCase):
    def test_windows_sections(self):
        analyzer = metadata.PEAnalyzer("tests/assets/hello.exe")
        self.assertTrue(len(analyzer.sections) > 0)
        self.assertTrue(b'.text' in analyzer.sections[0].Name)

    def test_linux_sections(self):
        analyzer = metadata.ELFAnalyzer("tests/assets/hello")
        self.assertTrue(len(analyzer.sections) > 0)
        self.assertTrue(analyzer.sections[1].name == '.interp')

    def test_windows_get_section_by_name(self):
        analyzer = metadata.PEAnalyzer("tests/assets/hello.exe")
        text_section = analyzer.get_section_by_name(".text")
        self.assertTrue(text_section is not None)
        self.assertTrue(b'.text' in text_section.Name)

    def test_linux_get_section_by_name(self):
        analyzer = metadata.ELFAnalyzer("tests/assets/hello")
        text_section = analyzer.get_section_by_name(".text")
        self.assertTrue(text_section is not None)
        self.assertTrue(text_section.name == ".text")

    def test_disassembly_windows(self):
        analyzer = metadata.PEAnalyzer("tests/assets/hello.exe")
        text_section = analyzer.get_section_by_name(".text")

        self.assertTrue(b'.text' in text_section.Name)
        
        instructions = analyzer.disassemble(text_section)
        self.assertTrue(len(instructions) > 0)
        self.assertTrue(instructions[0]["address"] == 0x140001000)
        self.assertTrue(instructions[-1]["address"] == 0x140002bff)

    def test_disassembly_linux(self):
        analyzer = metadata.ELFAnalyzer("tests/assets/hello")
        text_section = analyzer.executable.get_section_by_name(".text")

        self.assertTrue(text_section is not None)

        instructions = analyzer.disassemble(text_section)
        self.assertTrue(len(instructions) > 0)
        self.assertTrue(instructions[0]["address"] == 0x1040)
        self.assertTrue(instructions[-1]["address"] == 0x1152)