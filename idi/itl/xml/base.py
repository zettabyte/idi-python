# encoding: utf-8
from xml.etree import ElementTree as ET


class XmlValue:
    """Basic data value within exported iTunes Library (ITL) XML document"""

    def __init__(self, e):
        if not isinstance(e, ET.Element):
            raise ValueError("'e' must be a xml.etree.ElementTree.Element")
        if e.attrib:
            raise ValueError("XML element 'e' must not have any attributes")
        self.raw = e


class XmlLeafValue(XmlValue):
    """Basic leaf-node element value within ITL XML document; has no child elements/values"""

    def __init__(self, e):
        super().__init__(e)
        if len(e):
            raise ValueError("XML element 'e' must not have any child elements")

