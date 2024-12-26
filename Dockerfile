FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN apt update 
RUN apt install pkg-config python3-dev \
        default-libmysqlclient-dev \
        build-essential weasyprint -y

RUN apt install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT [ \
    "gunicorn", \
    "-w", \
    "1", \
    "-b", \
    ":8001", \
    "core.wsgi:application" \
]

EXPOSE 8001