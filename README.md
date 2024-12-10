# Pamas Quiz

![GitHub repo size](https://img.shields.io/github/repo-size/iuricode/README-template?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/iuricode/README-template?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/iuricode/README-template?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/bitbucket/issues/iuricode/README-template?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/iuricode/README-template?style=for-the-badge)

> Projeto para gera um Quiz aos usuários, que ao finalizar o questionário, gera um documento PDF com o resultado da pesquisa.

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- Python 3.12.0
- pip 24.2
- docker-compose version 1.28.0 

## 🚀 Instalando Pamas Quiz

Rodando apenas com o docker:

```
$ docker-compose exec web python manage.py makemigrations pagamentos quiz usuarios planos notificacoes
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py createsuperuser
$ docker-compose up
```

Para instalar o Pamas Quiz, siga estas etapas:

Linux :

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ docker-compose up -d
```

## ☕ Usando Pamas Quiz

Para usar Pamas Quiz, siga estas etapas:

```
python -m manage.py runserver
```

## Usando Makefile

Para facilitar operações do projeto siga:

- Criar um virtual env
```
$ make criar-env
```

- Remover um virtual env
```
$ make remover-env
```

- Instalar as libs do projeto
```
$ source venv/bin/activate
$ make instalar-libs
```

- Rodar o servicor
```
$ make run-server
```

- Rodar gunicorn wsgi
```
$ make run-gunicor-wsgi
```


## Referências / Templates

- [sb-admin-2](https://startbootstrap.com/previews/sb-admin-2)
- [bootstrap4](https://getbootstrap.com/docs/4.6/getting-started/introduction/)
