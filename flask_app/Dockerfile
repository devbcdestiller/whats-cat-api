FROM python:3.8.10

COPY . /flask_app
WORKDIR /flask_app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Use this entry point in development
# ENTRYPOINT ["python", "app.py"]

# Use this ENTRYPOINT and CMD production
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "app:app"]