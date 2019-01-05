# encoding: utf-8
from datetime import datetime
from xml.etree import ElementTree as ET

import pytest
import pytz

from idi.itl.xml import composite as xml_composite, scalar as xml_scalar


TEST_SCHEMA = {
    "Name": {
        "types"     : { "string": xml_scalar.String },
        "categories": {
            "Album"    : True,
            "Movie"    : True,
            "TV Show"  : True,
            "Audiobook": True,
            "Podcast"  : True,
        },
    },
    "Artist": {
        "types"     : { "string": xml_scalar.String },
        "categories": { "Album": True },
    },
    "Director": {
        "types"     : { "string": xml_scalar.String },
        "categories": { "Movie": False },
    },
    "Track Number": {
        "types"     : { "integer": xml_scalar.Integer },
        "categories": { "Album": False },
    },
    "Release Date": {
        "types": {
            "date"   : xml_scalar.DateTime,
            "integer": xml_scalar.Timestamp,
        },
        "categories": {
            "Album": True,
            "Movie": True,
            "Book" : True,
        },
    },
}


class TestDictionary:

    @pytest.mark.happypath
    def test_init__happy_path(self):
        e = ET.XML(
            """<dict>
                <key>Name</key>   <string>Foo</string>
                <key>Artist</key> <string>Bar</string>
            </dict>"""
        )
        assert xml_composite.Dictionary(e, schema=TEST_SCHEMA).value == "Album"

    def test_init__parameter_not_a_xml_dict_element__fails(self):
        e = ET.XML(
            """<array>
                <key>Name</key>   <string>Foo</string>
                <key>Artist</key> <string>Bar</string>
            </array>"""
        )
        with pytest.raises(ValueError):
            xml_composite.Dictionary(e, schema=TEST_SCHEMA)

    def test_init__parameter_is_a_xml_element__no_children__fails(self):
        e = ET.XML("<dict></dict>")
        with pytest.raises(ValueError):
            xml_composite.Dictionary(e, schema=TEST_SCHEMA)

    def test_init__parameter_is_a_xml_element__one_child__fails(self):
        e = ET.XML("<dict><key>Name</key></dict>")
        with pytest.raises(ValueError):
            xml_composite.Dictionary(e, schema=TEST_SCHEMA)

    def test_init__parameter_is_a_xml_element__odd_number_of_children__fails(self):
        e = ET.XML(
            """<dict>
                <key>Name</key>   <string>Foo</string>
                <key>Artist</key>
            </dict>"""
        )
        with pytest.raises(ValueError):
            xml_composite.Dictionary(e, schema=TEST_SCHEMA)

    def test_init__parameter_is_a_xml_element__has_leading_text__fails(self):
        e = ET.XML(
            """<dict>Text
                <key>Name</key>   <string>Foo</string>
                <key>Artist</key> <string>Bar</string>
            </dict>"""
        )
        with pytest.raises(ValueError):
            xml_composite.Dictionary(e, schema=TEST_SCHEMA)

    def test_init__parameter_is_a_xml_element__has_trailing_text__fails(self):
        e = ET.XML(
            """<dict>
                <key>Name</key>   <string>Foo</string>
                <key>Artist</key> <string>Bar</string>
                Text
            </dict>"""
        )
        with pytest.raises(ValueError):
            xml_composite.Dictionary(e, schema=TEST_SCHEMA)

    def test_init__parameter_is_a_xml_element__has_intermingled_text__fails(self):
        e = ET.XML(
            """<dict>
                <key>Name</key>   <string>Foo</string>
                Text
                <key>Artist</key> <string>Bar</string>
            </dict>"""
        )
        with pytest.raises(ValueError):
            xml_composite.Dictionary(e, schema=TEST_SCHEMA)

    def test_init__has_key_child_element_not_in_schema__fails(self):
        e = ET.XML(
            """<dict>
                <key>BadKey</key> <string>Foo</string>
                <key>Artist</key> <string>Bar</string>
            </dict>"""
        )
        with pytest.raises(ValueError):
            xml_composite.Dictionary(e, schema=TEST_SCHEMA)

    def test_init__has_value_child_element_tag_not_in_schema_for_associated_key_name__fails(self):
        e = ET.XML(
            """<dict>
                <key>Name</key>   <integer>0</integer>
                <key>Artist</key> <string>Bar</string>
            </dict>"""
        )
        with pytest.raises(ValueError):
            xml_composite.Dictionary(e, schema=TEST_SCHEMA)

    def test_init__combination_of_fields_matches_no_categories__fails(self):
        e = ET.XML(
            """<dict>
                <key>Name</key>     <string>Foo</string>
                <key>Artist</key>   <string>Bar</string>
                <key>Director</key> <string>Baz</string>
            </dict>"""
        )
        with pytest.raises(ValueError):
            xml_composite.Dictionary(e, schema=TEST_SCHEMA)

    def test_init__combination_of_fields_matches_multiple_categories__fails(self):
        e = ET.XML("<dict><key>Name</key><string>Foo</string></dict>")
        with pytest.raises(ValueError):
            xml_composite.Dictionary(e, schema=TEST_SCHEMA)

    @pytest.mark.parametrize(("e", "expected"), (
        ("<date>2010-01-02T03:04:05Z</date>", datetime(2010, 1, 2, 3, 4, 5, tzinfo=pytz.utc)),
        ("<integer>3471390245</integer>",     datetime(2010, 1, 2, 3, 4, 5, tzinfo=pytz.utc)),
    ))
    def test_init__schema_allows_alternate_types_for_some_fiels(self, e, expected):
        e = ET.XML(
            """<dict>
                <key>Name</key>   <string>Foo</string>
                <key>Artist</key> <string>Bar</string>
                <key>Release Date</key> {}
            </dict>""".format(e)
        )
        assert xml_composite.Dictionary(e, schema=TEST_SCHEMA)["Release Date"] == expected

