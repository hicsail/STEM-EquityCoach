FROM python:3.8-slim

# Set env to prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the app code to the working directory
COPY . /app/

# Expose the port the app runs on:
EXPOSE 5000

# Run the Flask application:
CMD ["python", "run.py"]