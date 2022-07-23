FROM python:3.10

EXPOSE 8088

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY dependencies/requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . /v1
COPY . /core
COPY . /configs

WORKDIR /v1

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /v1
USER appuser

CMD ["python", "main.py"]
