# encoding: utf-8
import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name                          = "idi",
    version                       = "0.0.1",
    author                        = "Kendall Gifford",
    author_email                  = "zettabyte@gmail.com",
    description                   = "I despise iTunes (idi) is an iTunes library tool",
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    url                           = "https://github.com/zettabyte/idi-python",
    packages                      = setuptools.find_packages(),
    classifiers                   = [
        "Development Status :: 1 - Planning",
        "Environment :: MacOS X",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Sound/Audio",
    ],
)
