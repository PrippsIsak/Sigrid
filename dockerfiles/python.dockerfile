FROM python:3.8-slim

WORKDIR /app

COPY backend/requirements.txt .
COPY backend/src .

RUN pip install -r requirements.txt --verbose

CMD [ "python", "./backend/src/main"]