FROM python:alpine3.18
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
USER 10101010
ENTRYPOINT ["gunicorn","--config", "gunicorn_conf.py", "main:app"]
