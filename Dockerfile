FROM python:3.11-alpine
LABEL maintainer="amiencoy"
LABEL description="Reconnator - Modern Cloud-Native Recon Bot"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
ENTRYPOINT ["python", "src/main.py"]