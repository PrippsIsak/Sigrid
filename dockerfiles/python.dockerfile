FROM python:3.8-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY backend/requirements.txt /app/
RUN pip install -r requirements.txt --verbose

# Copy the source code

COPY backend/src ./src
# Run the main Python script
CMD [ "python", "main.py"]
