# encoding: utf-8
"""
Scalar data types used for parsing and representing iTunes Library (ITL) details from exported XML file.

Part of the following class hierarchy:
  Value    (in idi.itl.xml.base)
    Scalar (in idi.itl.xml.base)
      ScalarEmpty
        Boolean
      ScalarRaw
        String
      ScalarValue
        Base64
        DateTime
        Integer
          NonNegativeInteger
            Timestamp
        Key
    Object (in idi.itl.xml.composite)
    Array  (in idi.itl.xml.composite)
"""
import base64
import binascii
from datetime import datetime, timedelta

import pytz

from idi.itl.xml import base as xml_base


class ScalarEmpty(xml_base.Scalar):
    """Basic empty (no text) scalar value (no children) whose 'value' is the underlying XML tag's name"""

    def __init__(self, e):
        super().__init__(e)
        if e.text:
            raise ValueError("XML element 'e' must be empty (no text content, not even whitespace)")
        self.value = e.tag


class Boolean(ScalarEmpty):
    """Basic empty (no text) scalar value (no children) that can be <true/> or <false/>"""

    def __init__(self, e):
        super().__init__(e)
        if self.value not in ("true", "false"):
            raise ValueError("XML element 'e' must be a <true/> or <false/> XML element")
        self.value = bool(self.value == "true")


class ScalarRaw(xml_base.Scalar):
    """Basic text-only scalar value (no children) whose 'value' is the XML element's raw text content"""

    def __init__(self, e):
        super().__init__(e)
        self.value = e.text


class String(ScalarRaw):
    """Basic scalar (no children) element with some possibly empty or whitespace-only text"""

    def __init__(self, e):
        super().__init__(e)
        if e.tag != "string":
            raise ValueError("XML element 'e' must be a <string> XML element")
        if self.value is None:
            self.value = ""


class ScalarValue(xml_base.Scalar):
    """Basic text-only scalar value (no children) that must have some non-whitespace content"""

    def __init__(self, e):
        super().__init__(e)
        if not e.text or not e.text.strip():
            raise ValueError("XML element 'e' must have some non-whitespace content")
        self.value = e.text.strip()


class Base64(ScalarValue):
    """Basic scalar (no children) having base64-encoded data text content"""

    def __init__(self, e):
        super().__init__(e)
        if e.tag != "data":
            raise ValueError("XML element 'e' must be an <data> XML element")
        try:
            self.value = base64.b64decode(self.value)
        except binascii.Error:
            raise ValueError("Content of XML element 'e' has invalid base64-encoding")


class DateTime(ScalarValue):
    """Basic scalar (no children) having a single YYYY-MM-DDTHH:MM:SSZ formated UTC date/time value"""

    def __init__(self, e):
        super().__init__(e)
        if e.tag != "date":
            raise ValueError("XML element 'e' must be a <date> XML element")
        self.value = datetime.strptime(self.value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)


class Integer(ScalarValue):
    """Basic scalar (no children) having a single decimal-encoded integer"""

    def __init__(self, e):
        super().__init__(e)
        if e.tag != "integer":
            raise ValueError("XML element 'e' must be an <integer> XML element")
        self.value = int(self.value)


class NonNegativeInteger(Integer):
    """Basic scalar (no children) having a single decimal-encoded integer that can't be negative"""

    def __init__(self, e):
        super().__init__(e)
        if self.value < 0:
            raise ValueError("XML element 'e' must have a non-negative integral value")


class Timestamp(NonNegativeInteger):
    """Basic scalar (no children) integer that's a UNIX-like timestamp based on 1900-01-01T00:00:00Z"""
    basis = datetime(1900, 1, 1, tzinfo=pytz.utc)

    def __init__(self, e):
        super().__init__(e)
        self.timestamp = self.value
        self.value     = self.basis + timedelta(seconds=self.timestamp)


class Key(ScalarValue):
    """Basic scalar (no children) element with a non-empty/non-whitespace-only textual key-name value"""

    def __init__(self, e):
        super().__init__(e)
        if e.tag != "key":
            raise ValueError("XML element 'e' must be a <key> XML element")

