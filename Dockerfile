FROM python:3.10.4-slim-buster

#default values for proxy host and port
ARG PROXY_HOST="127.0.0.1" 
ARG PORXY_PORT="8000"

ENV proxy_host=$PROXY_HOST 
ENV proxy_port=$PORXY_PORT 


# 
COPY ./src /app/src

# 
COPY ./requirements.txt /app

# 
WORKDIR /app

# 
RUN pip install -r requirements.txt

#
EXPOSE 8000
CMD uvicorn src.main:app --host ${proxy_host} --port ${proxy_port}
