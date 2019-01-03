# encoding: utf-8
import os

_version = None
def version():
    global _version
    if _version:
        return _version
    filename = os.path.abspath(os.path.join(os.path.dirname(__file__), "VERSION"))
    with open(filename, "r") as f:
        _version = tuple(int(x) for x in f.read().strip().split("."))
    return _version

