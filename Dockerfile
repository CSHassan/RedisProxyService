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
CMD ["uvicorn", "src.main:app","--reload"]
