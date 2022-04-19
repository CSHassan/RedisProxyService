run:
	python src/main.py
build: requirements.txt
	pip install -r requirements.txt
test:
	pytest
