FROM python:3.9

LABEL author="dmitriyvasil@gmail.com"

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python runserver.py