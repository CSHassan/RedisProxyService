# 
FROM python:3.9

# 
WORKDIR /app

# 
COPY requirements.txt /code/requirements.txt
COPY env.yaml /code/app

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./main.py  /code/app
COPY ./redis_backend.py  /code/app
# 
CMD ["uvicorn", "app.main:app", "--reload"]
