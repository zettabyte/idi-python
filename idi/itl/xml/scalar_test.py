# encoding: utf-8
from datetime import datetime
from xml.etree import ElementTree as ET

import pytest
import pytz

from idi.itl.xml import scalar as xml_scalar


class TestXmlBase64Value:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<data>SGVsbG8sIHdvcmxkLg==</data>")
        assert xml_scalar.XmlBase64Value(e).value == b"Hello, world."

    def test_init__parameter_not_a_xml_data_element__fails(self):
        e = ET.XML("<string>SGVsbG8sIHdvcmxkLg==</string>")
        with pytest.raises(ValueError):
            xml_scalar.XmlBase64Value(e)

    def test_init__parameter_is_a_xml_data_element__with_invalid_base64_content__fails(self):
        e = ET.XML("<data>SGVsbG8sIHdvcmxkLg</data>")
        with pytest.raises(ValueError):
            xml_scalar.XmlBase64Value(e)


class TestXmlBooleanValue:

    @pytest.mark.happypath
    def test_init__true__happy_path(self):
        e = ET.XML("<true/>")
        assert xml_scalar.XmlBooleanValue(e).value is True

    @pytest.mark.happypath
    def test_init__false__happy_path(self):
        e = ET.XML("<false/>")
        assert xml_scalar.XmlBooleanValue(e).value is False

    def test_init__parameter_not_a_xml_bool_element__fails(self):
        e = ET.XML("<foo/>")
        with pytest.raises(ValueError):
            xml_scalar.XmlBooleanValue(e)


class TestXmlDateTimeValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<date>2010-01-02T03:04:05Z</date>")
        assert xml_scalar.XmlDateTimeValue(e).value == datetime(2010, 1, 2, 3, 4, 5, tzinfo=pytz.utc)

    def test_init__parameter_not_a_xml_date_element__fails(self):
        e = ET.XML("<integer>2010-01-02T03:04:05Z</integer>")
        with pytest.raises(ValueError):
            xml_scalar.XmlDateTimeValue(e)

    @pytest.mark.parametrize("v", ("hello", "01/02/2010", "2010-01-02", "2010-01-02T03:04:05"))
    def test_init__parameter_is_a_xml_date_element__with_invalid_date_text__fails(self, v):
        # "invalid" here includes incomplete; being strict; requires exact format w/'Z' UTC timezone
        e = ET.XML("<date>{}</date>".format(v))
        with pytest.raises(ValueError):
            xml_scalar.XmlDateTimeValue(e)


class TestXmlEmptyValue:

    @pytest.mark.happypath
    @pytest.mark.parametrize("e", ("<empty/>", "<empty></empty>"))
    def test_init__happy_path(self, e):
        e = ET.XML(e)
        v = xml_scalar.XmlEmptyValue(e) # doesn't raise
        assert v.raw is e

    @pytest.mark.parametrize("e", ("<text>0</text>", "<whitepace1> </whitepace1>", "<ws2>\n</ws2>"))
    def test_init__parameter_is_a_xml_element__with_text__fails(self, e):
        e = ET.XML(e)
        with pytest.raises(ValueError):
            xml_scalar.XmlEmptyValue(e)

    def test_value__set_to_tag_name(self):
        e = ET.XML("<foo/>")
        assert xml_scalar.XmlEmptyValue(e).value == "foo"


class TestXmlIntegerValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<integer>42</integer>")
        assert xml_scalar.XmlIntegerValue(e).value == 42

    def test_init__parameter_not_a_xml_integer_element__fails(self):
        e = ET.XML("<string>42</string>")
        with pytest.raises(ValueError):
            xml_scalar.XmlIntegerValue(e)

    @pytest.mark.parametrize("v", ("hello", "x10", "3.14", "--42", "0xff"))
    def test_init__parameter_is_a_xml_integer_element__with_non_decimal_integral_text__fails(self, v):
        e = ET.XML("<integer>{}</integer>".format(v))
        with pytest.raises(ValueError):
            xml_scalar.XmlIntegerValue(e)


class TestXmlKeyValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<key>Name</key>")
        assert xml_scalar.XmlKeyValue(e).value == "Name"

    def test_init__parameter_not_a_xml_key_element__fails(self):
        e = ET.XML("<string>Name</string>")
        with pytest.raises(ValueError):
            xml_scalar.XmlKeyValue(e)


class TestXmlNonNegativeValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<integer>0</integer>")
        assert xml_scalar.XmlNonNegativeValue(e).value == 0

    def test_init__parameter_is_a_xml_integer_element__with_negative_value__fails(self):
        e = ET.XML("<integer>-1</integer>")
        with pytest.raises(ValueError):
            xml_scalar.XmlNonNegativeValue(e)


class TestXmlScalarValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<scalar>\n\tHello, world. \n</scalar>")
        assert xml_scalar.XmlScalarValue(e).value == "Hello, world."

    @pytest.mark.parametrize("e", ("<scalar/>", "<scalar></scalar>"))
    def test_init__parameter_is_an_empty_xml_element__fails(self, e):
        e = ET.XML(e)
        with pytest.raises(ValueError):
            xml_scalar.XmlScalarValue(e)

    @pytest.mark.parametrize("e", ("<scalar> </scalar>", "<scalar> \n \t \t \n </scalar>"))
    def test_init__parameter_is_an_xml_element_with_only_whitespace__fails(self, e):
        e = ET.XML(e)
        with pytest.raises(ValueError):
            xml_scalar.XmlScalarValue(e)

    @pytest.mark.parametrize(("e", "expected"), (
        ("<leading>  foo</leading>", "foo"),
        ("<trailing>bar  </trailing>", "bar"),
        ("<both>  baz  </both>", "baz"),
        ("<newlines>\n0\n</newlines>", "0"),
        ("<tabs>\t'quoted'\t</tabs>", "'quoted'"),
        ("<all> \n\t Inner space\n \tis\t \npreserved</all>", "Inner space\n \tis\t \npreserved"),
    ))
    def test_value__surrounding_whitespace_is_stripped(self, e, expected):
        e = ET.XML(e)
        assert xml_scalar.XmlScalarValue(e).value == expected


class TestXmlStringValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<string>Hello, world.</string>")
        assert xml_scalar.XmlStringValue(e).value == "Hello, world."

    @pytest.mark.parametrize("e", ("<string/>", "<string></string>"))
    def test_init__parameter_is_a_xml_string_element__empty_element_yields_empty_string(self, e):
        e = ET.XML(e)
        assert xml_scalar.XmlStringValue(e).value == ""

    def test_init__parameter_not_a_xml_string_element__fails(self):
        e = ET.XML("<integer>Hi</integer>")
        with pytest.raises(ValueError):
            xml_scalar.XmlStringValue(e)


class TestXmlTextValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<text>Hello, world.</text>")
        assert xml_scalar.XmlTextValue(e).value == "Hello, world."

    @pytest.mark.parametrize("e", ("<empty/>", "<empty></empty>"))
    def test_init__parameter_is_an_empty_xml_element__value_is_none(self, e):
        e = ET.XML(e)
        assert xml_scalar.XmlTextValue(e).value is None

    @pytest.mark.parametrize("e", ("<ws1> </ws1>", "<ws2>\n</ws2>"))
    def test_init__parameter_is_a_whitespace_only_xml_element__value_is_string(self, e):
        e = ET.XML(e)
        v = xml_scalar.XmlTextValue(e)
        assert isinstance(v.value, str)
        assert v.value.strip() == ""


class TestXmlTimestampValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        expected = datetime(2010, 1, 2, 3, 4, 5, tzinfo=pytz.utc)
        value    = int((expected - datetime(1900, 1, 1, tzinfo=pytz.utc)).total_seconds())
        e        = ET.XML("<integer>{}</integer>".format(value))
        assert xml_scalar.XmlTimestampValue(e).value == expected

    def test_timestamp__original_timestamp_integral_value(self):
        e = ET.XML("<integer>42</integer>")
        assert xml_scalar.XmlTimestampValue(e).timestamp == 42

