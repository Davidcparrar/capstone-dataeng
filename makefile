SOURCEDIR = src
TESTSDIR = tests

install:
	pip install --upgrade -r requirements.txt
	
test:
	python -m pytest -vv --cov=$(SOURCEDIR) $(TESTSDIR)/

lint:
	pylint --disable=R,C $(SOURCEDIR)/

format:
	black -l 79 .

sort:
	isort .

clean
	rm $(SOURCEDIR)/logs/*.log

all: install format sort lint test