# Use the official Python image as a base
FROM python:3.11

# Set the working environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the application's working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirement.txt /app/
RUN pip install --upgrade pip && pip install -r requirement.txt

# Copy the application content into the container
COPY . /app/

# Expose the port used by the application
EXPOSE 8000

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "docicpdfbackend.wsgi:application"]
