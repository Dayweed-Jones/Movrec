#Pull base immage
FROM python:3.10.4-bullseye

#Set enviroment variables
ENV PIP_DISSABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Set work direcotry
WORKDIR /web 

#Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#Copy project
COPY . .