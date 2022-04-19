run:
	python src/main.py
setup: requirements.txt
	pip install -r requirements.txt
test:
	pytest
