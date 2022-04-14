# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY requirements.txt /code/requirements.txt
COPY env.yaml /code/app

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY main /code/app
COPY redis_backend /code/app
# 
CMD ["hypercorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
