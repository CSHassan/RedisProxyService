run:
	python src/main.py
build: requirements.txt
	pip3 install -r requirements.txt
test:
	python3 -m unittest discover -s ./tests/ -p '*_test.py'
