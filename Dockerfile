FROM python:3.10.13-slim

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./app /app

CMD [ "python", "/app/app.py" ]