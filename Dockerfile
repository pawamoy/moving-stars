FROM python:3.6-alpine

RUN pip install requests

COPY move_stars.py /run.py

CMD ["python", "/run.py"]

