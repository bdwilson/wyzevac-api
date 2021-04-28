FROM python:3.9-slim-buster

ARG WYZEVAC_USER
ARG WYZEVAC_PASS
ARG WYZEVAC_PORT=59354

RUN mkdir /code
WORKDIR /code

RUN apt-get update -y && \
    apt-get install -y git && \
    pip install flask wyze_sdk && \
	git clone https://github.com/bdwilson/wyzevac-api && \
	sed -i "s/WYZEVAC_USER/${WYZEVAC_USER}/" /code/wyzevac-api/wyzevac_flask.py && \
	sed -i "s/WYZEVAC_PASS/${WYZEVAC_PASS}/" /code/wyzevac-api/wyzevac_flask.py && \
	sed -i "s/WYZEVAC_PORT/${WYZEVAC_PORT}/" /code/wyzevac-api/wyzevac_flask.py

#ADD . /code/
EXPOSE ${WYZEVAC_PORT}
CMD [ "python3.9", "/code/wyzevac-api/wyzevac_flask.py" ]
