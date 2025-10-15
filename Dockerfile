# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# The --no-cache-dir flag is a good practice for keeping image sizes small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code into the container
# This copies the application, templates, and any static files into the container.
COPY app.py .
COPY templates/ ./templates/ 
COPY static/ ./static/

# Make port 8080 available to the world outside this container
# Cloud Run uses this to route requests to your app.
EXPOSE 8080

# Define the command to run your app.
CMD ["python", "app.py"]