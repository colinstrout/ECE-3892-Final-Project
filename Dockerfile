# Base Image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy model and source code
COPY t5-small-onnx ./t5-small-onnx
COPY app.py .
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make container accept command line arguments
ENTRYPOINT ["python", "app.py"]