FROM ubuntu:xenial
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir \
    celery==3.1.24 \
    flask==0.12.2 \
    flask_api==1.0 \
    pymongo==3.6.1 \
    sqlalchemy==1.1.13 \
    sqlalchemy_vertica==0.2.5 \
    vertica_python==0.7.3 \
    psycopg2==2.7.4 \
    PyYAML==3.12 \
    cryptography==2.1.4
RUN pip3 install --no-cache-dir \
    uwsgi==2.0.17
WORKDIR /usr/src/app
COPY . .
RUN chmod -R a+rwx .
ENTRYPOINT [ "./entrypoint.sh" ]
