# producer/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY producer.py producer.py
COPY wait-for-kafka.sh wait-for-kafka.sh
RUN chmod +x wait-for-kafka.sh

EXPOSE 4000

CMD ["python", "producer.py"]
