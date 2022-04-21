run:
	python3 src/main.py
build: requirements.txt
	pip install -r requirements.txt
test:
	pip install -r requirements.txt	
	python3 -m unittest discover -s ./tests/ -p '*_test.py'
