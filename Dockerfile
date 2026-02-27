FROM python:3.11-slim-bookworm

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies early to cache them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image
COPY . .

# Run the web service on container startup.
# Cloud Run expects the app to listen on port $PORT (default 8080)
CMD streamlit run app.py --server.port=${PORT:-8080} --server.address=0.0.0.0
