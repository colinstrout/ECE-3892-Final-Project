# 1. Base Image
FROM python:3.12-slim

# 2. Set working directory
WORKDIR /app

# # 3. Install BUILD TOOLS (Forced for ARM64 compatibility)
# # We need these to compile the psutil C-extensions
# RUN apt-get update && apt-get install -y \
#     gcc \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# 4. Copy ONLY requirements first for caching
COPY requirements.txt .

# 5. Install dependencies
# Using --prefer-binary can sometimes help pip find a wheel if it exists
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy model and source code LAST
COPY ./models /app/models
COPY app.py .

# 7. Environment variables and Entrypoint
ENV ARCH=amd64

ENTRYPOINT ["python", "app.py"]