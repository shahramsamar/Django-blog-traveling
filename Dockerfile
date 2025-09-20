# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Maintainer information
LABEL maintainer="Shahramsamar2010@gmail.com"


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && python -m pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/
