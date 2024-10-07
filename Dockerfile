# Use an official Python runtime as a parent image
FROM python:3.12

# Install necessary system packages, including Tesseract and additional language packs
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-fra \
    tesseract-ocr-spa

ENV HOST=0.0.0.0
ENV LISTEN_PORT 8000
EXPOSE 8000

# Set the working directory in the container
WORKDIR /app

# Install pipx for managing poetry or pip-tools
RUN pip install --upgrade pip

# Ensure the tessdata folder is set to /usr/share/tessdata
ENV TESSDATA_PREFIX=/usr/share/tessdata

# Copy the requirements.txt file
COPY requirements.txt ./

# Install dependencies using poetry
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .