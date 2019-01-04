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


class XmlBase64Value(XmlValue):
    def __init__(self, e):
        super().__init__(e)
        if e.tag != "data":
            raise ValueError("XML element 'e' must be an <data> XML element")
        if len(e):
            raise ValueError("XML element 'e' must not have any child elements")
        if not e.text:
            raise ValueError("XML element 'e' must have text content")
        data = e.text.strip()
        if not data:
            raise ValueError("XML element 'e' must have non-whitespace text content")
        try:
            self.value = base64.b64decode(data)
        except binascii.Error:
            raise ValueError("Content of XML element 'e' has invalid base64-encoding")


class XmlBoolValue(XmlValue):
    def __init__(self, e):
        super().__init__(e)
        if e.tag not in { "true", "false" }:
            raise ValueError("XML element 'e' must be a <true/> or <false/> XML element")
        if len(e):
            raise ValueError("XML element 'e' must not have any child elements")
        if e.text:
            raise ValueError("XML element 'e' must not have text content")
        self.value = bool(e.tag == "true")


class XmlDateTimeValue(XmlValue):
    def __init__(self, e):
        super().__init__(e)
        if e.tag != "date":
            raise ValueError("XML element 'e' must be a <date> XML element")
        if len(e):
            raise ValueError("XML element 'e' must not have any child elements")
        if not e.text:
            raise ValueError("XML element 'e' must have text content")
        self.value = datetime.strptime(e.text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)


class XmlIntValue(XmlValue):
    def __init__(self, e):
        super().__init__(e)
        if e.tag != "integer":
            raise ValueError("XML element 'e' must be an <integer> XML element")
        if len(e):
            raise ValueError("XML element 'e' must not have any child elements")
        if not e.text:
            raise ValueError("XML element 'e' must have text content")
        self.value = int(e.text)


class XmlNNIntValue(XmlIntValue):
    """Non-Negative (>= 0) Integer Value"""
    def __init__(self, e):
        super().__init__(e)
        if self.value < 0:
            raise ValueError("XML element 'e' must have a non-negative integral value")


class XmlStrValue(XmlValue):
    def __init__(self, e):
        super().__init__(e)
        if e.tag != "string":
            raise ValueError("XML element 'e' must be a <string> XML element")
        if len(e):
            raise ValueError("XML element 'e' must not have any child elements")
        self.value = e.text if e.text else ""


class XmlTimestampValue(XmlNNIntValue):
    """Integer representing a UNIX epoch timestamp; main value converted to said value"""
    basis = datetime(1900, 1, 1, tzinfo=pytz.utc)

    def __init__(self, e):
        super().__init__(e)
        self.timestamp = self.value
        self.value     = self.basis + timedelta(seconds=self.timestamp)

