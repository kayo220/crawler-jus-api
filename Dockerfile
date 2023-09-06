FROM python:3.11.5
# copy the requirements file into the image
# switch working directory
WORKDIR /app

RUN apt-get update -y
# RUN apt-get -y python-pip python-dev
# install the dependencies and packages in the requirements file
# RUN pip install --upgrade pip
RUN pip install flask
RUN pip install flask_restx
RUN pip install pytest
RUN pip install python-dotenv
RUN pip install scrapy

# copy every content from the local file to the image
COPY . .

EXPOSE 5000
# configure the container to run in an executed manner
# ENTRYPOINT [ "python" ]
CMD ["flask", "run", "--host", "0.0.0.0"]