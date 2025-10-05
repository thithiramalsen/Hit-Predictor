# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies that might be needed by your Python packages
# (e.g., OpenCV dependencies for easyocr)
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

# Expose the port the app runs on and command to run the app
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8080"]