FROM python:3.9-alpine

WORKDIR /usr/src/app

EXPOSE 5000

ENV FLASK_APP=src
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt ./
RUN pip install -r requirements.txt --quiet

COPY . .

CMD ["flask", "run"]