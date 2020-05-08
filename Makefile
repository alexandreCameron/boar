include .makefile_env
export .makefile_env

help: ## Help recipies listing all the recipies of Makefile
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/##//'
.PHONY: help

# Install python
# --------------

install-python:  ## Install python dependencies
	@echo "+++install:"
	${PIP} install --no-cache-dir -r requirements/${ENV_REQUIREMENTS}.txt
	${PIP} install --no-cache-dir -e .
.PHONY: install

# Commitlint
# ----------

install-commitlint:  ## Install commitlint dependencies 
	@echo "+++install-commitlint:"
	@echo "On local machine use sudo to install dependencies"
	@if [ $(node -v) ]; then\
		apt-get install nodejs npm;\
	fi
	npm install -g @commitlint/cli @commitlint/config-conventional
.PHONY: install-commitlint

commitlint:  ## Launch commitlint
	@echo "+++commitlint"
	@echo "On WSL you have to format the script file:"
	@echo "dos2unix commitlint/lint.sh"
	bash commitlint/lint.sh ${BRANCH_NAME} ${ENV_EXECUTION}
.PHONY: commitlint

# Markdown lint
# -------------

install-markdownlint:  ## Install markdownlint dependencies 
	@echo "+++install-markdown-lint:"
	npm install -g markdownlint-cli
.PHONY: install-markdown-lint

markdownlint:  ## Launch markdown lint
	@echo "+++markdown-lint:"
	markdownlint '*.md' --config .markdownlint.json
.PHONY: markdown-lint


# JS-lint
# -------

lints-js:  ## Run JS lints
	${MAKE} commitlint
	${MAKE} markdownlint
.PHONY: lints-js

# ============
# Python tests
# ============

# Lint
# ----

test-flake8:  ## Launch python linter
	@echo "+++test-flake8:"
	flake8 ${PROJECT_PATH} ${TEST_PATH} ${NOTEBOOK_TEST_PATH} *.py
.PHONY: test-flake8

# Doc
# ---

convert-md2rst:  ## Convert markdown to rst for the doc
	m2r --overwrite ${FILE}.md ${FILE}.rst && mv ${FILE}.rst ${DOC_PATH}
.PHONY: convert-md2rst

build-doc:  ##  Build python documentation using sphinx
	@echo "+++build-doc:"
	sphinx-build -T -E -b readthedocs -d ${DOC_PATH}/.build/doctrees-readthedocs -D language=en ${DOC_PATH}/ ${DOC_PATH}/.build/html
.PHONY: build-doc

# Unit tests
# ----------

test-pytest:  ## Launch python tests
	@echo "+++test-pytest:"
	${PYTEST} ${TEST_PATH} -m "ut" --cov-report=xml
	${PYTEST} ${TEST_PATH} -m "e2e"
	${PYTEST} ${TEST_PATH} -m "tuto"
.PHONY: test-pytest

tests-python:  ## Launch all python tests
	@echo "+++tests:"
	${MAKE} test-flake8
	${MAKE} build-doc
	${MAKE} test-pytest
.PHONY: tests-python

# =====
# Tests
# =====

tests-all: ## Run all tests
	${MAKE} lints-js
	${MAKE} tests-python
.PHONY: tests-all

# =======
# Release
# =======

release:  ## Create wheel
	@echo "+++release:"
	rm ./dist/*
	sed -i "s/version=\"[0-9].[0-9].[0-9]\"/version=\"${VERSION}\"/g" setup.py
	${PYTHON} setup.py sdist bdist_wheel
.PHONY: release

publish-testpypi:  ## Publish package on testpypi
	@echo "+++publish-testpypi:"
	${PYTHON} -m twine upload --repository testpypi dist/* --verbose
.PHONY: publish-testpypi

publish-pypi:  ## Publish package on pypi
	@echo "+++publish-pypi:"
	${PYTHON} -m twine upload dist/*
.PHONY: publish-pypi
