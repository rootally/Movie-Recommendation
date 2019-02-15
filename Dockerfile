#docker file for Movie-R
FROM ubuntu
MAINTAINER amitj646@gmail.com
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip install numpy flask flask_login flask_mongoengine pandas
CMD ["echo","Image created"]
