FROM python

WORKDIR /src/backend

COPY requirement.txt .
COPY src .

RUN pip install -r requirement.txt

CMD [ "python", "./backend/src/main"]

