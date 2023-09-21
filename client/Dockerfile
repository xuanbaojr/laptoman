FROM python:3.9-slim

ARG GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

WORKDIR /app

COPY . /app

RUN set -x \
    && apt-get update \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python -m pip install -U --no-cache-dir --default-timeout=100 pip && pip install --no-cache-dir --upgrade -r /app/requirements.txt --default-timeout=100

CMD ["gradio", "app_gradio.py"]