FROM python:3.12.3-alpine AS backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV OPENAI_API_KEY=$OPENAI_API_KEY_KALIBRE

RUN apk update && apk add --no-cache \
    build-base \
    gfortran \
    musl-dev \
    postgresql-dev \
    python3-dev \
    libffi-dev

RUN pip install --upgrade pip setuptools

WORKDIR /code
COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install psycopg2-binary

COPY . /code/

# Expose the port for the application
EXPOSE 800


CMD gunicorn economics_project.wsgi:application --whitenoise --bind 0.0.0.0:8000
