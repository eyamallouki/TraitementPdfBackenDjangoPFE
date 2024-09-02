FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copying the requirements file first to leverage Docker cache
COPY requirements.txt /app/

# Upgrade pip and install dependencies with increased timeout to prevent network timeout issues
RUN pip install --upgrade pip && \
    pip install --default-timeout=1000 -r requirements.txt && \
    pip install pymupdf python-docx

# Installing system dependencies, including Tesseract with French language pack
RUN apt-get update && \
    apt-get install -y poppler-utils \
                       tesseract-ocr \
                       tesseract-ocr-eng \
                       tesseract-ocr-fra && \
    rm -rf /var/lib/apt/lists/*

# Set the TESSDATA_PREFIX environment variable correctly
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/

# Copy the rest of your application
COPY . /app/

# Expose port if needed
# EXPOSE 8000

# Command to run your application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
