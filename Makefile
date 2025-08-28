SHELL := /bin/bash

migrate:
	python3 manage.py migrate

migrations:
	python3 manage.py makemigrations

run:
	python3 manage.py runserver

freeze:
	pip3 freeze > requirements.txt

superuser:
	python3 manage.py createsuperuser

setup:
	python3 manage.py migrate
	python3 manage.py runscript initial_setup
	python3 manage.py createsuperuser

