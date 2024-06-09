FROM python:3.12.1

RUN apt-get update && \
    apt-get install -yq tzdata
ENV TZ="Asia/Yekaterinburg"

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .


