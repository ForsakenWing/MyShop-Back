FROM python:3.10-slim

EXPOSE 8100

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY dependencies/requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /v1
COPY . /core

WORKDIR /v1

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /v1
USER appuser

CMD ["uvicorn", "--host=0.0.0.0", "--port=8100", "v1.api:app"]
