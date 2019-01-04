# encoding: utf-8
import base64
import binascii
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

import pytz


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


class XmlEmptyValue(XmlLeafValue):
    """Basic leaf-node empty element value within ITL XML document; has no children or content"""

    def __init__(self, e):
        super().__init__(e)
        if e.text:
            raise ValueError("XML element 'e' must be empty (no text content, not even whitespace)")
        self.value = e.tag


class XmlTextValue(XmlLeafValue):
    """Basic leaf-node element that may be empty or may have text content"""

    def __init__(self, e):
        super().__init__(e)
        self.value = e.text


class XmlScalarValue(XmlLeafValue):
    """Basic leaf-node element with some non-whitespace text content; surrounding whitespace stripped"""

    def __init__(self, e):
        super().__init__(e)
        if not e.text or not e.text.strip():
            raise ValueError("XML element 'e' must have some non-whitespace content")
        self.value = e.text.strip()


class XmlBase64Value(XmlScalarValue):
    def __init__(self, e):
        super().__init__(e)
        if e.tag != "data":
            raise ValueError("XML element 'e' must be an <data> XML element")
        try:
            self.value = base64.b64decode(self.value)
        except binascii.Error:
            raise ValueError("Content of XML element 'e' has invalid base64-encoding")


class XmlBoolValue(XmlEmptyValue):
    def __init__(self, e):
        super().__init__(e)
        if self.value not in { "true", "false" }:
            raise ValueError("XML element 'e' must be a <true/> or <false/> XML element")
        self.value = bool(self.value == "true")


class XmlDateTimeValue(XmlScalarValue):
    def __init__(self, e):
        super().__init__(e)
        if e.tag != "date":
            raise ValueError("XML element 'e' must be a <date> XML element")
        self.value = datetime.strptime(self.value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)


class XmlIntValue(XmlScalarValue):
    def __init__(self, e):
        super().__init__(e)
        if e.tag != "integer":
            raise ValueError("XML element 'e' must be an <integer> XML element")
        self.value = int(self.value)


class XmlKeyValue(XmlScalarValue):
    def __init__(self, e):
        super().__init__(e)
        if e.tag != "key":
            raise ValueError("XML element 'e' must be a <key> XML element")


class XmlNNIntValue(XmlIntValue):
    """Non-Negative (>= 0) Integer Value"""
    def __init__(self, e):
        super().__init__(e)
        if self.value < 0:
            raise ValueError("XML element 'e' must have a non-negative integral value")


class XmlStringValue(XmlTextValue):
    def __init__(self, e):
        super().__init__(e)
        if e.tag != "string":
            raise ValueError("XML element 'e' must be a <string> XML element")
        if self.value is None:
            self.value = ""


class XmlTimestampValue(XmlNNIntValue):
    """Integer representing a UNIX-like timestamp based on 1900-01-01T00:00:00Z"""
    basis = datetime(1900, 1, 1, tzinfo=pytz.utc)

    def __init__(self, e):
        super().__init__(e)
        self.timestamp = self.value
        self.value     = self.basis + timedelta(seconds=self.timestamp)

