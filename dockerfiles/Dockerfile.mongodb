FROM mongo:latest

WORKDIR /usr/src

COPY mongo_setup/mongo.key .

COPY mongo_setup/product_mock.json .

RUN chmod 400 mongo.key && chown mongodb:mongodb mongo.key