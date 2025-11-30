VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
REQ = requirements.txt

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r $(REQ)

run:
	$(PYTHON) main.py

run-debug:
	$(PYTHON) main.py --debug
