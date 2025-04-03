# Use an official Python image as the base
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY stock-backend .

# Expose port 5000 (default for Flask)
EXPOSE 5000

# Set environment variable to tell Flask it's in production mode
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the Flask application using Gunicorn
# You can adjust the number of workers based on your instance size
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]