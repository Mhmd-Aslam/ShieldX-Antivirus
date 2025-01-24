from static.metadata import PEAnalyzer

analyzer = PEAnalyzer("./tests/assets/hello.exe")
for symbol in analyzer.import_symbols:
  print(symbol.dll)