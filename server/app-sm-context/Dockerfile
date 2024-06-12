FROM python:3.8-slim

# Set env to prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG OLLAMA_URL
ARG GOOGLE_DRIVE_FOLDER_ID
ARG JSON_CREDS

ENV OLLAMA_URL=${OLLAMA_URL}
ENV GOOGLE_DRIVE_FOLDER_ID=${GOOGLE_DRIVE_FOLDER_ID}

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Create the .credentials directory and pass the credentials content
RUN mkdir -p /root/.credentials
COPY credentials.json /root/.credentials/credentials.json
# RUN echo ${JSON_CREDS} > /root/.credentials/credentials.json

# Set environment variables for Google credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=/root/.credentials/credentials.json

# Copy the content of the app code to the working directory
COPY . /app/

# Expose the port the app runs on:
EXPOSE 5000

# Run the Flask application:
CMD ["python", "run.py"]