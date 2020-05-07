.PHONY: prepare run test

install-requirements:
	apt-get install -y python3.8 python3-pip python3.8-venv;

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
