# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory in the container
WORKDIR /spotify2MP3

# Copy the current directory contents into the container at /spotify2MP3
COPY . /spotify2MP3

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg (needed for youtube-dl)
RUN apt-get update && \
    apt-get install -y ffmpeg

# Copy .env file to the container
COPY .env .env

# Set environment variables
ENV FLASK_APP=app.py
RUN export $(xargs < .env)

# Expose port 5000 to allow communication to/from server
EXPOSE 5000

# Run the flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
