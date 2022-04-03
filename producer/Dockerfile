# # basic python image
# FROM python:3.7

# # install pika to access rabbitmq
# RUN pip install pika
# RUN pip install requests
# RUN pip install flask

# # Without this setting, Python never prints anything out.
# ENV PYTHONUNBUFFERED=1

# # declare the source directory
# WORKDIR /usr/src/app/producer
# # copy the file
# COPY producer.py .

# EXPOSE 5005
# # start command
# CMD [ "python", "producer.py"]

# https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
# https://x-team.com/blog/set-up-rabbitmq-with-docker-compose/

FROM python:3.8.10-alpine3.13

#RUN mkdir -p /usr/src
WORKDIR /usr/src/app/producer

ENV PYTHONUNBUFFERED=1
#set python
RUN python3 -m pip install --upgrade pip
RUN pip install virtualenv
RUN virtualenv cc_env
RUN . cc_env/bin/activate

# install dependencies 
RUN pip install pika
RUN pip install uuid
RUN pip install Flask

EXPOSE 5005

#RUN Python
CMD ["python3", "-u", "producer.py"]