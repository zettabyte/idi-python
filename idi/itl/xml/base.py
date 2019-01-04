# encoding: utf-8
"""
Base data types used for parsing and representing iTunes Library (ITL) details from exported XML file.
"""
from xml.etree import ElementTree as ET


class Value:
    """Basic data value within exported iTunes Library (ITL) XML document (scalar or composite)"""

    def __init__(self, e):
        if not isinstance(e, ET.Element):
            raise ValueError("'e' must be a xml.etree.ElementTree.Element")
        if e.attrib:
            raise ValueError("XML element 'e' must not have any attributes")
        self.raw = e


class Scalar(Value):
    """Basic leaf-node (no children) data value within exported iTunes Library (ITL) XML document"""

    def __init__(self, e):
        super().__init__(e)
        if len(e):
            raise ValueError("XML element 'e' must not have any child elements")

