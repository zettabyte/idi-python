# encoding: utf-8
VERSION_FILE := idi/VERSION
VERSION      := $(shell cat ${VERSION_FILE})

DIST_DIR         := dist
BUILD_DIR        := build
EGG_INFO_DIR     := idi.egg-info
PYTEST_CACHE_DIR := .pytest_cache

SOURCE_DIST := $(DIST_DIR)/idi-$(VERSION).tar.gz
WHEEL_DIST  := $(DIST_DIR)/idi-$(VERSION)-py3-none-any.whl

META_DEPS := README.md LICENSE setup.cfg setup.py $(VERSION_FILE)
CODE_DEPS := $(shell find idi -name '*.py')

.PHONY: help all push push-test clean
.DEFAULT: help

help:
	@echo "make all"
	@echo "    build all standard artifacts"
	@echo "make push"
	@echo "    push latest collection of built artifacts to pypi"
	@echo "make push-test"
	@echo "    push latest collection of built artifacts to pypi test environment"
	@echo "make clean"
	@echo "    remove intermediate build and test files as well as old built artifacts"
	@echo "make help"
	@echo "    display this help message"

all: $(SOURCE_DIST) $(WHEEL_DIST)

push: $(SOURCE_DIST) $(WHEEL_DIST)
	pipenv run twine upload "$(SOURCE_DIST)" "$(WHEEL_DIST)"

push-test: $(SOURCE_DIST) $(WHEEL_DIST)
	pipenv run twine upload --repository-url https://test.pypi.org/legacy/ "$(SOURCE_DIST)" "$(WHEEL_DIST)"

$(SOURCE_DIST): $(META_DEPS) $(CODE_DEPS)
	pipenv run python setup.py sdist

$(WHEEL_DIST): $(META_DEPS) $(CODE_DEPS)
	pipenv run python setup.py bdist_wheel

clean:
	rm -rf $(DIST_DIR)/
	rm -rf $(BUILD_DIR)/
	rm -rf $(EGG_INFO_DIR)/
	rm -rf $(PYTEST_CACHE_DIR)/

