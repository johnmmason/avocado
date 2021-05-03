FROM python:3.9

COPY source /app
WORKDIR /app
RUN ln -sf /usr/share/zoneinfo/America/Chicago /etc/localtime
RUN pip install -r requirements.txt

CMD ["python3", "-u", "/app/worker.py"]
