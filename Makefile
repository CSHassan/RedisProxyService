run:
	python3 src/main.py
build: requirements.txt
	pip install -r requirements.txt
test:
	docker-compose up
stop:
	docker-compose down
