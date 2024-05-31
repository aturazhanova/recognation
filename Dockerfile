FROM python:3.11-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    make \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your application code
COPY . .

# Set environment variables
ENV HOST 0.0.0.0

# Expose the port your application will run on
EXPOSE 5001

# Command to run the application
CMD ["python", "withphoto.py"]