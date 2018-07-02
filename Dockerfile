FROM python:3.6-alpine

RUN pip install moving-stars

CMD ["move-stars"]

