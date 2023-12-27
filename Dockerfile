# Use Python 3.11 as the base image
FROM tiangolo/uvicorn-gunicorn:python3.11

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN echo "Requirements installed"

# Populate the db
CMD ["python", "/scripts/create_data.py"]

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
