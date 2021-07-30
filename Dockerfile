FROM python:3.8

WORKDIR /flask-blog

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./app ./app

CMD [ "python", "./app/run.py" ]