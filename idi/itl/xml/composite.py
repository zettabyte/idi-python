# encoding: utf-8
from idi.itl import schema as default_schema
from idi.itl.xml.base import Value
from idi.itl.xml.scalar import Key


class Dictionary(Value):
    """XML element containing key/value tag pairs where key names are unique"""

    def __init__(self, e, schema=None):
        super().__init__(e)
        if e.tag != "dict":
            raise ValueError("XML element 'e' must be a <dict> XML element")

        if schema is None:
            schema = default_schema.DEFAULT
        self.schema   = schema
        self.children = list(e)
        self.__dict   = {}

        if not self.children:
            raise ValueError("XML element 'e' must have at least two child elements")
        if len(self.children) % 2:
            raise ValueError("XML element 'e' must have an even number of child elements")
        if (e.text and e.text.strip()) or any(c.tail and c.tail.strip() for c in self.children):
            raise ValueError("XML element 'e' must not have any text content")

        categories = self.__load_fields()
        if len(categories) > 1:
            raise ValueError(
                "Combination of child element key/values is ambiguous; "
                "possible categories are: {}".format(", ".join(sorted(list(categories))))
            )
        self.value = categories.pop()

    def __load_fields(self):
        name                = None # state tracking variable for loop below
        possible_categories = None # a set of strings or None; return value
        for child in self.children:
            if name is None:
                name = Key(child).value
            else:
                value, possible_categories = self.__load_field(name, child, possible_categories)
                self.__dict[name] = value
                name = None
        return possible_categories

    def __load_field(self, name, e, possible_categories):
        if name not in self.schema:
            raise ValueError("Unknown child XML element found (name '{}' not in schema)".format(name))
        if e.tag not in self.schema[name]:
            raise ValueError("Child element with name '{}' has invalid tag '{}'".format(name, e.tag))
        klass, categories = self.schema[name][e.tag]
        if possible_categories is None:
            possible_categories = categories
        else:
            possible_categories = possible_categories & categories
        if not possible_categories:
            raise ValueError("Combination of child element key/values invalid")
        return klass(e), possible_categories

    def __getitem__(self, key):
        return self.__dict[key].value

