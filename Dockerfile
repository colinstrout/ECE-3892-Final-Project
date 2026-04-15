# Base Image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Only run apt-get if INSTALL_BUILD_TOOLS is true
RUN if [ "$INSTALL_BUILD_TOOLS" = "true" ] ; then \
    apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* ; \
    fi

COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy model and source code
COPY ./models /app/models
COPY app.py .

ENV ARCH=amd64
# Make container accept command line arguments
ENTRYPOINT ["python", "app.py"]