FROM python:3.8.10

ADD . /flask_server
WORKDIR /flask_server

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "./flask_server/app.py"]
