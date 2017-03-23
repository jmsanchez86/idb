.DEFAULT_GOAL := test

FILES :=                 \
	app/models.py \
	app/tests.py  \
	apiary.apib          \
	.gitignore           \
	.travis.yml          \
	README               \
	IDB1.html            \
	IDB1.log             \
	IDB1.pdf             \
	makefile

# Apple
ifeq ($(shell uname), Darwin)
	PYTHON   := python3.5
	PIP      := pip3.5
	PYLINT   := pylint
	COVERAGE := coverage-3.5
	PYDOC    := pydoc3.5
	AUTOPEP8 := autopep8
# Travis CI
else ifeq ($(CI), true)
	PYTHON   := python3.5
	PIP      := pip3.5
	PYLINT   := pylint
	COVERAGE := coverage-3.5
	PYDOC    := pydoc3.5
	AUTOPEP8 := autopep8
# Docker
else ifeq ($(shell uname -p), unknown)
	PYTHON   := python3.5
	PIP      := pip3.5
	PYLINT   := pylint
	COVERAGE := coverage-3.5
	PYDOC    := pydoc3.5
	AUTOPEP8 := autopep8
# UTCS
else
	PYTHON   := python3
	PIP      := pip3
	PYLINT   := pylint
	COVERAGE := coverage-3.5
	PYDOC    := pydoc3.5
	AUTOPEP8 := autopep8
endif

.PHONY: versions
versions:
	which make
	make --version
	@echo
	which git
	git --version
	@echo
	which $(PYTHON)
	$(PYTHON) --version
	@echo
	which $(PIP)
	$(PIP) --version
	@echo
	which $(PYLINT)
	$(PYLINT) --version
	@echo
	which $(COVERAGE)
	$(COVERAGE) --version
	@echo
	-which $(PYDOC)
	-$(PYDOC) --version
	@echo
	which $(AUTOPEP8)
	$(AUTOPEP8) --version
	@echo
	$(PIP) list

.PHONY: check
check: static-check
	@not_found=0;                                 \
	for i in $(FILES);                            \
	do                                            \
		if [ -e $$i ];                            \
		then                                      \
			echo "$$i found";                     \
		else                                      \
			echo "$$i NOT FOUND";                 \
			not_found=`expr "$$not_found" + "1"`; \
		fi                                        \
	done;                                         \
	if [ $$not_found -ne 0 ];                     \
	then                                          \
		echo "$$not_found failures";              \
		exit 1;                                   \
	fi;                                           \
	echo "success";

.pylintrc:
	$(PYLINT) --disable=locally-disabled \
			  --reports=no \
			  --generated-members=query,Integer,Column,String,ForeignKey,relationship,Float\
			  --generate-rcfile > $@

.PHONY: test
test: .pylintrc
	$(PYLINT) app/tests.py
	$(PYTHON) app/tests.py

.PHONY: format
format:
	$(AUTOPEP8) -i app/models.py
	$(AUTOPEP8) -i app/tests.py

MYPY_SOURCES := $(shell find ./app -name '*.py')
mypy-check: $(MYPY_SOURCES)
	mypy --ignore-missing-imports $(MYPY_SOURCES)

pylint-check: $(MYPY_SOURCES)
	$(PYLINT) $(MYPY_SOURCES)

static-check: mypy-check pylint-check

IDB1.html:
	pydoc3 -w IDB1

IDB1.log:
	git log > IDB1.log

.PHONY: all
all: IDB1.html IDB1.log
	make format
	make run
	make test
	make check
