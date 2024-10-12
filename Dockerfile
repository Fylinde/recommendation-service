FROM python:3.9

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip

# Install essential system dependencies
RUN apt-get update && apt-get install -y \
    nano \
    curl \
    postgresql-client \
    iputils-ping \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    python3-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Install Cython and NumPy separately to make them available for pystan
RUN pip install --no-cache-dir Cython numpy

RUN pip install --no-cache-dir prophet 

RUN pip install transformers==4.30.2

RUN pip install alembic 

RUN pip install email-validator

# Install scikit-surprise
RUN pip install scikit-surprise

# Install Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app /app/app
COPY start.sh /app/start.sh
COPY wait-for-it.sh /app/wait-for-it.sh

# Make start.sh script executable
RUN chmod +x /app/start.sh

# Expose the application port
EXPOSE 8006

# Command to run the application
CMD ["/app/start.sh"]
