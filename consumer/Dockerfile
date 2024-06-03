FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY consumer.py consumer.py

EXPOSE 4000

CMD ["python", "consumer.py"]
