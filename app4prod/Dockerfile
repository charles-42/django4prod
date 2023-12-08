# pull official base image
FROM python:3.9-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# copy project
COPY . /app

#RUN python manage.py collectstatic --noinput

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["gunicorn", "--bind", ":8000", "app4prod.wsgi:application"]