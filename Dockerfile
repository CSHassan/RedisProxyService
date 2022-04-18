FROM python:3.10.4-slim-buster

# 
COPY ./src /app/src

# 
COPY ./requirements.txt /
COPY ./env.yaml  /

# 
WORKDIR /app

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt



# 
CMD ["uvicorn", "src.main:app","--reload"]
