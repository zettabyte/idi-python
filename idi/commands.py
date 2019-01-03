# encoding: utf-8
from idi import version

def main():
    print("idi v{}".format(".".join(str(x) for x in version)))
    return 0

