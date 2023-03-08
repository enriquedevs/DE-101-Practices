# Use the official Python 3.10 image as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install Java
RUN apt-get update && apt-get install -y default-jdk

# Copy the requirements file into the container
COPY requirements.txt .

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Update OS libraries and install VI editor
RUN apt-get update && apt-get install -y vim

# Default command that is triggered when container starts
CMD ["tail", "-f", "/dev/null"]
