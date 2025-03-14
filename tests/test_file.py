from hooktest.tester import Parser
import os.path

op = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

p = Parser()
p.ingest([op("./test_data/catalog.xml")])
p.tests()
