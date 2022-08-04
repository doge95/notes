FROM python:3.7-slim

RUN mkdir /app
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD *.py /app/
CMD ["opentelemetry-instrument", "python", "/app/app.py"]