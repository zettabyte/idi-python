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
    keywords                      = "itunes music library metadata",
    packages                      = setuptools.find_packages(),
    setup_requires                = ["pytest-runner>=4.2,<5"],
    tests_require                 = ["pytest>=4.0.2,<=5"],
    install_requires              = ["mutagen>=1.42.0,<2"],
    python_requires               = "~=3.7",
    entry_points                  = { "console_scripts": ["idi = idi.commands:main"] },
    url                           = "https://github.com/zettabyte/idi-python",
    project_urls = {
        "Source": "https://github.com/zettabyte/idi-pythpon/",
        "Bugs"  : "https://github.com/zettabyte/idi-pythpon/issues",
    },
    classifiers = [
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
