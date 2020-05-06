.PHONY: prepare run test

prepare:
	python3.8 -m venv venv; \
	. venv/bin/activate; \
	pip install -r requirements.txt;

run:
	. venv/bin/activate; \
	export PYTHONPATH=$PYTHONPATH:$(pwd); \
	python3.8 server.py

test:
	. venv/bin/activate; \
    python -m unittest discover -s test -p test*.py;
