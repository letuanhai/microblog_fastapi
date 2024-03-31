FROM python:alpine3.19

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app

CMD [ "uvicorn", "main:app", "--reload" ]