FROM python:3.8.10-buster

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]