# Using image Python3
FROM python:3
ENV PYTHONUNBUFFERED 1

# Create directory
RUN mkdir /code

# Setting working directory
WORKDIR /code

# Add files to working directory
ADD requirements.txt /code/

# Run commands to install
RUN pip install -r requirements.txt
ADD . /code/
