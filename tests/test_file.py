from hooktest.tester import Tester
import os.path

op = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

p = Tester()
p.ingest([op("./test_data/catalog.xml")])
p.tests()
print(p.results)
