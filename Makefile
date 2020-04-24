include .makefile_env
export .makefile_env

help: ## Help recipies listing all the recipies of Makefile
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/##//'
.PHONY: help

# Install python
# --------------

install-python:  ## Install python dependencies on azure feed or pypi repo
	@echo "+++install:"
	${PIP} install --no-cache-dir -r requirements/${ENV_REQUIREMENTS}.txt
	${PIP} install --no-cache-dir -e .
.PHONY: install

# Commitlint
# ----------

install-commitlint:  ## Install node dependencies for commitlint
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

install-markdownlint:
	@echo "+++install-markdown-lint:"
	npm install -g markdownlint-cli
.PHONY: install-markdown-lint

markdownlint:
	@echo "+++markdown-lint:"
	markdownlint '**/*.md' --config .markdownlint.json
.PHONY: markdown-lint


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

build-doc:  ##  Build python documentation using sphinx
	@echo "+++build-doc:"
	sphinx-build -Wb html ${DOC_PATH} ${DOC_PATH}/.build
.PHONY: build-doc

# Unit tests
# ----------

test-pytest:  ## Launch python tests
	@echo "+++test-pytest-ut:"
	${PYTEST} ${TEST_PATH}
.PHONY: test-pytest

tests-pytest:  ## Launch all  python tests
	@echo "+++tests:"
	${MAKE} test-flake8
	${MAKE} build-doc
	${MAKE} test-pytest
.PHONY: tests-pytest

# Release
# -------

release:  ## Launch wheel creation
	@echo "+++release:"
	sed -i "s/version=\"[0-9].[0-9].[0-9]\"/version=\"${VERSION}\"/g" setup.py
	${PYTHON} setup.py bdist_wheel
.PHONY: release
