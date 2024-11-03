.ONESHELL:

PROJECT_NAME=pamas


remover-venv:
	@ echo 'Removendo venv'
	rm -rf venv
	@ echo 'venv removido!'

criar-venv: remover-venv
	@ echo 'Criando venv'
	python -m venv venv
	@ echo 'venv criado!'

instalar-libs:
	@ echo 'Instalando libs do $PROJECT_NAME'
	pip install -r requirements.txt
	@ echo 'libs instaladas!'

clear-cache:
	@ echo 'Limpando __pycache__'
	rm -rf */__pycache__
	@ echo '__pycache__ limpo!'

run-server:
	python manage.py runserver

run-gunicorn-wsgi:
	gunicorn core.wsgi