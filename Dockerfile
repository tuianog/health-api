FROM python:3.11-slim

# install PostgreSQL client
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

WORKDIR /api
ADD . /api/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt

# EXPOSE 8082

# WORKDIR /api/api
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]