FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN set -x \
    && apt-get update 

RUN python -m pip install -U --no-cache-dir --default-timeout=100 pip && pip install --no-cache-dir --upgrade -r /app/requirements.txt --default-timeout=100

CMD ["uvicorn", "model_api:app", "--host", "0.0.0.0", "--port", "8000"]