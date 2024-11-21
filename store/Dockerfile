FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY reg.txt /app/
RUN pip install gunicorn
RUN pip install setuptools
RUN pip install --upgrade pip && \
    pip install -r reg.txt

COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY . /app/