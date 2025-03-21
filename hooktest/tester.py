import dataclasses
from typing import Dict, List, Optional
from collections import Counter

from dapitains.tei.citeStructure import CitableUnit
from dapitains.tei.document import Document
from dapitains.metadata.xml_parser import parse, Catalog


@dataclasses.dataclass
class Log:
    name: str
    status: bool
    exception: Optional[Exception | str] = None
    details: Optional[str] = None

    def __repr__(self):
        return f"<Log class='{self.name}' status={self.status}>{self.details}</Log>"

@dataclasses.dataclass
class Result:
    target: str
    statuses: List[Log] = dataclasses.field(default_factory=list)

    def __repr__(self):
        return f"<Result target='{self.target}'>\n\t{"\n".join(["\t"+repr(log) for log in self.statuses])}\n</Result>"


def _count_tree(units: List[CitableUnit], types = None) -> str:
    types = types if types is not None else {}
    for element in units:
        if element.citeType not in types:
            types[element.citeType] = {
                "count": 0,
                "children": {}
            }
        types[element.citeType]["count"] += 1
        _count_tree(element.children, types[element.citeType]["children"])
    return types


def _stringify_tree_count(tree) -> str:
    return ", ".join([
        f"{level}({details['count']})" + (
            f"->[{_stringify_tree_count(details['children'])}]" if details["children"]
            else ""
        )
        for level, details in tree.items()
    ])


class Parser:
    """
    >>> p = Parser()
    >>> p.ingest(["/home/tclerice/dev/MyDapytains/tests/catalog/example-collection.xml"])
    >>> p.results
    >>> p.tests()
    """
    def __init__(self):
        self.catalog = Catalog()
        self.results: Dict[str, Result] = {}

    def ingest(self, files: List[str]):
        for file in files:
            try:
                before = len(self.catalog.relationships)
                _, collection = parse(file, self.catalog)
                self.results[file] = Result(
                    file, [
                        Log("parse", True),
                        Log(
                            "relationships", True,
                            details="+ {0} element(s)".format(len(self.catalog.relationships) - before)
                        ),
                        Log(
                            "children", True,
                            details="{0} child(ren)".format(len([
                                pair
                                for pair in self.catalog.relationships
                                if collection.identifier in pair
                            ]))
                        )
                    ]
                )
            except Exception as E:
                self.results[file] = Result(file, [Log("parse", False, E)])

        print("{} collection(s) found".format(len(self.catalog.objects)))
        print("{} resource(s) found".format(len([o for o in self.catalog.objects.values() if o.resource])))

    def tests(self):
        resources = [o for o in self.catalog.objects.values() if o.resource]
        for r in resources:
            doc = Document(r.filepath)
            print(f"{r.identifier}: {len(doc.citeStructure)} tree(s)")
            trees = "\n".join([
                f"Tree:{tree}->{_stringify_tree_count(_count_tree(doc.get_reffs(tree)))}"
                for tree in doc.citeStructure
                ])
            print(trees)
