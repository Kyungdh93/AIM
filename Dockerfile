FROM bitnami/python:3.10.12

RUN pip install --upgrade pip

# Install netcat
RUN apt-get update && apt-get install -y netcat

WORKDIR /fastapi-mysql

COPY ./requirements.txt /fastapi-mysql/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /fastapi-mysql/requirements.txt

COPY ./app /fastapi-mysql/app

# Add entrypoint.sh
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set entrypoint to wait for MySQL server
ENTRYPOINT ["/entrypoint.sh"]