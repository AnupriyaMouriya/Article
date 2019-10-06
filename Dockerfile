FROM ubuntu:18.04

RUN mkdir /app

COPY . /app

WORKDIR /app


RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get install -y libpq-dev

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3","app.py"]
