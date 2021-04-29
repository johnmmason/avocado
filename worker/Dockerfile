FROM python:3.9

COPY . /app
WORKDIR /app
RUN ln -sf /usr/share/zoneinfo/America/Chicago /etc/localtime
RUN pip3 install -r requirements.txt

CMD ["python3", "/app/worker.py"]
