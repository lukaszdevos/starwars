install:
	pip install -r requirements.txt

build:
	python manage.py migrate

runserver:
	python manage.py runserver 8001

clean_code:
	black .
	isort .