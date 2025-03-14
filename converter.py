"""

pip install git+https://github.com/distributed-text-services/MyDapytains.git mycapytain
"""
import lxml.etree as et
import re
from typing import List
from dapitains.tei.document import Document
from MyCapytain.resources.texts.local.capitains.cts import CapitainsCtsText


def flattenReffs(elements) -> List[str]:
    """ Reffs in Dapitains are in a tree, so we need to flatten it (recursively)

    """
    els = [
        els for ref in elements
        for els in [ref.ref] + flattenReffs(ref.children)
    ]
    return els


def turnIntoCiteStructure(elements: List[et.ElementBase], levels: List[int], previous: str = "") -> str:
    """ Turn a list of refsDecl into a tree of citeStructure.
    They need to be in order (highest to deepest)
    """
    if levels[0] == 0:
        levels = [l+1 for l in levels]
    current = elements.pop(0)

    level = levels.pop(0)
    use = re.findall(r"([^\[]+)='?\$"+str(level)+r"'?", current.attrib["replacementPattern"])[0]
    match = current.attrib["replacementPattern"].replace("tei:", "")
    if "#xpath(" in match:
        match = match[7:-1]
    newprevious = match
    match = match.replace(previous, "")
    if previous:
        match = match.strip("/")
    match = re.sub(f'{use}=[\'\"]?'+r'\$\d[\'\"]?', "", match).replace("[]", "")
    cs = f"""<citeStructure use="{use}" match="{match}" unit="{current.attrib['n']}" {'delim="."' if level > 1 else ''}>"""
    if elements:
        cs += f"""\n{"\t"*level}{turnIntoCiteStructure(elements, levels, newprevious)}\n{"\t"*(level-1)}"""
    return cs + f"""</citeStructure>"""


def convert(file: str) -> str:
    """ Convert a Capitains file into a Dapitains file
    """
    base = et.parse(file)
    refsDecl = base.xpath("//t:refsDecl[@n='CTS']", namespaces={"t": "http://www.tei-c.org/ns/1.0"})

    if not refsDecl:
        return et.tostring(base, encoding=str)

    refsDecl = refsDecl[0]
    levels = {}

    for element in refsDecl:
        l = [int(el) for el in re.findall(r"\$(\d+)", element.attrib["replacementPattern"])][-1]
        levels[l] = element

    citeStructure = et.fromstring("""<TEI xmlns="http://www.tei-c.org/ns/1.0">\n<refsDecl>"""+turnIntoCiteStructure(
        [levels[i] for i in sorted(levels.keys())],
        levels=sorted(levels.keys())
    )+"""\n</refsDecl>\n</TEI>""")[0]

    refsDecl.getparent().replace(refsDecl, citeStructure)

    return et.tostring(base, encoding=str)

def convert_and_check(input_path: str, output_path: str) -> bool:
    with open(output_path, "w") as f:
        f.write(convert(input_path))

    doc = Document(output_path)
    citeReffs = sorted(flattenReffs(doc.get_reffs()))

    doc = CapitainsCtsText(
        resource=et.parse(input_path)
    )
    ctsReffs = sorted([
        str(citation)
        for level in range(1, len(doc.citation)+1)
        for citation in doc.getReffs(level=level)
        if citation
    ])

    return ctsReffs == citeReffs


import os


print(convert_and_check(
    "/home/tclerice/Downloads/tlg0004.tlg001.perseus-grc2(1).xml",
    os.path.join(os.path.dirname(__file__), "tests/test_data/tlg0004.tlg001.perseus-grc2.xml")
))