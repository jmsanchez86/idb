.DEFAULT_GOAL := test

PY_SOURCE := $(shell find ./app -name '*.py')
FILES :=                 \
	app/api/models.py    \
	app/api/test/tests.py\
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
	PYTHON   := python3.5
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
check:
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
	-$(PYLINT) app/api/test/tests.py
	-$(COVERAGE) run app/api/test/tests.py > app/api/test/tests.out 2>&1
	-$(COVERAGE) report -m                    >> app/api/test/tests.out
	rm .coverage

.PHONY: format
format:
	@not_found=0;                                 \
	for i in $(PY_SOURCE);                        \
	do                                            \
		$(AUTOPEP8) -i "$$i";                     \
	done;                                         \
	fi


mypy-check: $(PY_SOURCE)
	mypy --ignore-missing-imports $(PY_SOURCE)

pylint-check: $(PY_SOURCE)
	$(PYLINT) $(PY_SOURCE)

static-check: mypy-check pylint-check

IDB1.html:
	$(PYDOC) -w app.models
	mv app.models.html IDB1.html

IDB1.log:
	git log > IDB1.log

.PHONY: all
all: IDB1.html IDB1.log
	make format
	make test
	make check
