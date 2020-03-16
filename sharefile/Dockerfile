# pull official base image
FROM python:3.7-alpine

# set work directory
WORKDIR /home/teymur/Desktop/file_sharing_app/sharefile

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc libffi-dev python3-dev musl-dev libevent-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /home/teymur/Desktop/file_sharing_app/sharefile/requirements.txt
RUN pip install -r requirements.txt 

# copy project
COPY . /home/teymur/Desktop/file_sharing_app/sharefile/
