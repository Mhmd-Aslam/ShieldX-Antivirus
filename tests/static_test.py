import unittest
from static import metadata

class TestStatic(unittest.TestCase):
    def test_file_hashing(self):
        analyzer = metadata.StaticAnalyzer("tests/assets/CoronaVirus.exe")

        self.assertTrue(analyzer.hashes["md5"] == "055d1462f66a350d9886542d4d79bc2b")

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

    def test_get_import_symbol_by_name(self):
        analyzer = metadata.PEAnalyzer("tests/assets/hello.exe")
        symbol = analyzer.get_import_symbol_by_name("KERNEL32.dll")

        self.assertTrue(symbol.dll == b'KERNEL32.dll')

        imports = [imp.name for imp in symbol.imports]
        self.assertTrue(b"FreeLibrary" in imports)

    def test_import_symbols_windows(self):
        analyzer = metadata.PEAnalyzer("tests/assets/hello.exe")
        
        self.assertTrue(analyzer.import_symbols[0].dll == b'KERNEL32.dll')

    def test_symbols_linux(self):
        analyzer = metadata.ELFAnalyzer("tests/assets/hello")

        self.assertTrue("puts" in [symbol.name for symbol in analyzer.symbols])