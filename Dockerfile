FROM python:3.10.4-slim-buster

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
CMD ["uvicorn", "src.main:app"]
