FROM python:3.9.6-alpine

WORKDIR /app

COPY . .

RUN rm messages.log
RUN pip install pika

RUN apk add --no-cache openssl
ENV DOCKERIZE_VERSION v0.6.1

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

EXPOSE 5672:5672
EXPOSE 15672:15672

CMD ["python3","recv.py"]
