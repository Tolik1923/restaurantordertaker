FROM python:3.11

WORKDIR /code/app

COPY requirements.txt /code/app/requirements.txt

RUN pip install --no-cache-dir -r /code/app/requirements.txt

COPY . /code/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-dir", "/code/app"]

