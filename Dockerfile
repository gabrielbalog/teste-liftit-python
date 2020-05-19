# pull official base image
FROM python:3.8.0

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# update dependencies
RUN apt-get update && apt-get install netcat -y \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# create user
RUN useradd -ms /bin/bash app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]