# encoding: utf-8
import base64
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

import pytest
import pytz

from idi.itl.primitives import (
    XmlBase64Value,
    XmlBoolValue,
    XmlDateTimeValue,
    XmlEmptyValue,
    XmlIntValue,
    XmlLeafValue,
    XmlNNIntValue,
    XmlStrValue,
    XmlTimestampValue,
    XmlValue,
)


class TestXmlValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<element/>")
        XmlValue(e) # doesn't raise

    @pytest.mark.parametrize("e", ("string", 0, None, True, False, 3.14))
    def test_init__parameter_not_a_xml_element__fails(self, e):
        with pytest.raises(ValueError):
            XmlValue(e)

    def test_init__parameter_is_a_xml_element__with_attributes__fails(self):
        e = ET.XML("<element one='attribute'></element>")
        with pytest.raises(ValueError):
            XmlValue(e)

    def test_raw__holds_reference_to_original_xml_element_provided_to_init(self):
        e = ET.XML("<foo>stuff<bar>\nmoar\n<baz/></bar>and things</foo>")
        v = XmlValue(e)
        assert v.raw == e
        assert v.raw is e


class TestXmlBase64Value:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<data>SGVsbG8sIHdvcmxkLg==</data>")
        assert XmlBase64Value(e).value == b"Hello, world."

    def test_init__parameter_not_a_xml_data_element__fails(self):
        e = ET.XML("<string>SGVsbG8sIHdvcmxkLg==</string>")
        with pytest.raises(ValueError):
            XmlBase64Value(e)

    def test_init__parameter_is_a_xml_data_element__empty_element__fails(self):
        e = ET.XML("<data/>")
        with pytest.raises(ValueError):
            XmlBase64Value(e)

    @pytest.mark.parametrize("v", ("", " ", " \n ", "SGVsbG8sIHdvcmxkLg"))
    def test_init__parameter_is_a_xml_data_element__with_invalid_b64_byte_strings__fails(self, v):
        e = ET.XML("<data>{}</data>".format(v))
        with pytest.raises(ValueError):
            XmlBase64Value(e)


class TestXmlBoolValue:

    @pytest.mark.happypath
    def test_init__true__happy_path(self):
        e = ET.XML("<true/>")
        assert XmlBoolValue(e).value is True

    @pytest.mark.happypath
    def test_init__false__happy_path(self):
        e = ET.XML("<false/>")
        assert XmlBoolValue(e).value is False

    def test_init__parameter_not_a_xml_bool_element__fails(self):
        e = ET.XML("<foo/>")
        with pytest.raises(ValueError):
            XmlBoolValue(e)


class TestXmlDateTimeValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<date>2010-01-02T03:04:05Z</date>")
        assert XmlDateTimeValue(e).value == datetime(2010, 1, 2, 3, 4, 5, tzinfo=pytz.utc)

    def test_init__parameter_not_a_xml_date_element__fails(self):
        e = ET.XML("<integer>2010-01-02T03:04:05Z</integer>")
        with pytest.raises(ValueError):
            XmlDateTimeValue(e)

    def test_init__parameter_is_a_xml_date_element__empty_element__fails(self):
        e = ET.XML("<date/>")
        with pytest.raises(ValueError):
            XmlDateTimeValue(e)

    @pytest.mark.parametrize("v", ("", " ", "hello", "01/02/2010", "2010-01-02", "2010-01-02T03:04:05"))
    def test_init__parameter_is_a_xml_date_element__with_invalid_date_text__fails(self, v):
        # "invalid" here includes incomplete; being strict; requires exact format w/'Z' UTC timezone
        e = ET.XML("<date>{}</date>".format(v))
        with pytest.raises(ValueError):
            XmlDateTimeValue(e)


class TestXmlEmptyValue:

    @pytest.mark.happypath
    @pytest.mark.parametrize("e", ("<empty/>", "<empty></empty>"))
    def test_init__happy_path(self, e):
        e = ET.XML(e)
        v = XmlEmptyValue(e) # doesn't raise
        assert v.raw is e

    @pytest.mark.parametrize("e", ("<text>0</text>", "<whitepace1> </whitepace1>", "<ws2>\n</ws2>"))
    def test_init__parameter_is_a_xml_element__with_text__fails(self, e):
        e = ET.XML(e)
        with pytest.raises(ValueError):
            XmlEmptyValue(e)


class TestXmlIntValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<integer>42</integer>")
        assert XmlIntValue(e).value == 42

    def test_init__parameter_not_a_xml_integer_element__fails(self):
        e = ET.XML("<string>42</string>")
        with pytest.raises(ValueError):
            XmlIntValue(e)

    def test_init__parameter_is_a_xml_integer_element__empty_element__fails(self):
        e = ET.XML("<integer/>")
        with pytest.raises(ValueError):
            XmlIntValue(e)

    @pytest.mark.parametrize("v", ("", " ", "hello", "x10", "3.14", "--42", "0xff"))
    def test_init__parameter_is_a_xml_integer_element__with_non_decimal_integral_text__fails(self, v):
        e = ET.XML("<integer>{}</integer>".format(v))
        with pytest.raises(ValueError):
            XmlIntValue(e)


class TestXmlLeafValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<leaf>value</leaf>")
        v = XmlLeafValue(e) # doesn't raise
        assert v.raw is e

    def test_init__parameter_is_a_xml_element__with_children__fails(self):
        e = ET.XML("<parent>value<child/></parent>")
        with pytest.raises(ValueError):
            XmlLeafValue(e)


class TestXmlNNIntValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<integer>0</integer>")
        assert XmlNNIntValue(e).value == 0

    def test_init__parameter_is_a_xml_integer_element__with_negative_value__fails(self):
        e = ET.XML("<integer>-1</integer>")
        with pytest.raises(ValueError):
            XmlNNIntValue(e)


class TestXmlStrValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<string>Hello, world.</string>")
        assert XmlStrValue(e).value == "Hello, world."

    def test_init__parameter_is_a_xml_string_element__empty_element_yields_empty_string(self):
        e1 = ET.XML("<string/>")
        e2 = ET.XML("<string></string>")
        assert XmlStrValue(e1).value == ""
        assert XmlStrValue(e2).value == ""

    def test_init__parameter_not_a_xml_string_element__fails(self):
        e = ET.XML("<integer>Hi</integer>")
        with pytest.raises(ValueError):
            XmlStrValue(e)


class TestXmlTimestampValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        expected = datetime(2010, 1, 2, 3, 4, 5, tzinfo=pytz.utc)
        value    = int((expected - datetime(1900, 1, 1, tzinfo=pytz.utc)).total_seconds())
        e        = ET.XML("<integer>{}</integer>".format(value))
        assert XmlTimestampValue(e).value == expected

    def test_timestamp__original_timestamp_integral_value(self):
        e = ET.XML("<integer>42</integer>")
        assert XmlTimestampValue(e).timestamp == 42

