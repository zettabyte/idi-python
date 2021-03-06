# encoding: utf-8
"""
Base data types used for parsing and representing iTunes Library (ITL) details from exported XML file.

Even though another sibling module, 'scalar', may seem more appropriate for the 'Scalar' class
contained within this module, this 'Scalar' class is a base-class (though not enforcing it as
a pure ABC) while the 'scalar' module holds concrete types.

Part of the following class hierarchy:
  Value
    Scalar
      ScalarEmpty            (in idi.itl.xml.scalar)
        Boolean              (in idi.itl.xml.scalar)
      ScalarRaw              (in idi.itl.xml.scalar)
        String               (in idi.itl.xml.scalar)
      ScalarValue            (in idi.itl.xml.scalar)
        Base64               (in idi.itl.xml.scalar)
        DateTime             (in idi.itl.xml.scalar)
        Integer              (in idi.itl.xml.scalar)
          NonNegativeInteger (in idi.itl.xml.scalar)
            Timestamp        (in idi.itl.xml.scalar)
        Key                  (in idi.itl.xml.scalar)
    Object                   (in idi.itl.xml.composite)
    Array                    (in idi.itl.xml.composite)
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

