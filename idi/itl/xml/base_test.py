# encoding: utf-8
from xml.etree import ElementTree as ET

import pytest

from idi.itl.xml import base as xml_base


class TestValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<element/>")
        xml_base.Value(e) # doesn't raise

    @pytest.mark.parametrize("e", ("string", 0, None, True, False, 3.14))
    def test_init__parameter_not_a_xml_element__fails(self, e):
        with pytest.raises(ValueError):
            xml_base.Value(e)

    def test_init__parameter_is_a_xml_element__with_attributes__fails(self):
        e = ET.XML("<element one='attribute'></element>")
        with pytest.raises(ValueError):
            xml_base.Value(e)

    def test_raw__holds_reference_to_original_xml_element_provided_to_init(self):
        e = ET.XML("<foo>stuff<bar>\nmoar\n<baz/></bar>and things</foo>")
        v = xml_base.Value(e)
        assert v.raw == e
        assert v.raw is e


class TestXmlLeafValue:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML("<leaf>value</leaf>")
        v = xml_base.XmlLeafValue(e) # doesn't raise
        assert v.raw is e

    def test_init__parameter_is_a_xml_element__with_children__fails(self):
        e = ET.XML("<parent>value<child/></parent>")
        with pytest.raises(ValueError):
            xml_base.XmlLeafValue(e)

