# Use official Python 3.12 base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    unzip \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libxss1 \
    libxtst6 \
    xauth \
    xvfb \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy project files to container
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install playwright and required browsers
RUN playwright install --with-deps

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
