######################################################################################
# Dockerfile to build blog server with gnunicorn
# Based on UBUNTU
######################################################################################

# set the base image to UBUNTU
FROM python:3

# Author
MAINTAINER Sagar Sharma

# Set default work dir
WORKDIR /blog_server

# Copy the application folder inside the container
COPY requirements.txt ./

# install requirements
RUN pip install -r requirements.txt

# Expose ports
EXPOSE 9000

COPY . .

# start the server
# CMD ["gunicorn" "-w", "4", "application:boot", "--bind=0.0.0.0:9000"]
CMD ["./start.sh"]
