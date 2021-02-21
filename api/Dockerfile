# I was running into issues installing black during the pip install when running using 
# python:3.9-alpine image. if I had more time I'd explore getting this working with with
# alpine image. See: https://github.com/psf/black/issues/1106  
FROM python:3.9

WORKDIR /usr/src/app

EXPOSE 5000

ENV FLASK_APP=chat_app
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt ./
RUN pip install -r requirements.txt --quiet --no-cache-dir

COPY . .

CMD ["flask", "run"]