# encoding: utf-8
from pkg_resources import resource_string
version = tuple(int(x) for x in resource_string(__name__, "VERSION").decode("utf-8").strip().split("."))
