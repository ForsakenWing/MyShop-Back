FROM python:3.8-slim

EXPOSE 8100

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /application
COPY . /application

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /application
USER appuser

CMD ["uvicorn", "--host=0.0.0.0", "--port=8100", "application.server:app"]
