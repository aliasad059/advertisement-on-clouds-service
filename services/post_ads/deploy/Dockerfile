# pull official python image
FROM python:3.8-slim

# set working directory
ENV DockerHome=/home/services

RUN apt-get update && apt-get install g++ build-essential -y && apt-get clean

# create the working directory
RUN mkdir -p ${DockerHome}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy the working directory
COPY requirements.txt ${DockerHome}

# set the working directory
WORKDIR ${DockerHome}

# install the dependencies
RUN pip install --upgrade pip

RUN --mount=type=cache,target=/root/.cache \
	pip install -r requirements.txt
    
# copy the working directory
COPY . ${DockerHome}

# add pythonpath
ENV PYTHONPATH ${DockerHome}

# run the service
CMD cd ${DockerHome}/src && python main.py