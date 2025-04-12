FROM python:3.9-slim

WORKDIR /app

COPY . /app

# Install only required system packages safely
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "new.py", "--server.port=8501", "--server.address=0.0.0.0"]
