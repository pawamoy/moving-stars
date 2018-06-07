FROM python:3.6-alpine

RUN pip install requests colorama

COPY copy_stars.py /run.py

CMD ["python", "/run.py"]
