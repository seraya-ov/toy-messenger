FROM python:3.8

ENV DATABASE_URL postgresql://postgres:password@messenger:5432/messenger

RUN pip3 install --no-cache-dir psycopg2 flask Flask-SQLAlchemy Flask-Migrate

ADD . usr/src/app

EXPOSE 5000

CMD ["python3", "/usr/src/app/app.py"]
