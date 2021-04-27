FROM python:3.9


COPY source /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["worker.py"]

