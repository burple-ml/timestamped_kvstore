FROM python:3.12-slim

# Set working directory
WORKDIR /home

# Copy application files
COPY timestamped_kvstore /home/timestamped_kvstore

# Environment setup
COPY requirements.txt /home/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && rm -rf requirements.txt

EXPOSE 8080

# Run the application
CMD ["uvicorn", "timestamped_kvstore.app:app", "--host", "0.0.0.0", "--port", "8080"]
