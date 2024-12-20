FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN apt update 
RUN apt install pkg-config python3-dev default-libmysqlclient-dev build-essential weasyprint -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]