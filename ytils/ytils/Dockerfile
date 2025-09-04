FROM python:3.11

RUN apt-get update && apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY app /app

COPY app/requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

EXPOSE 5001

WORKDIR /

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5001", "--reload", "--reload-dir", "/app/"]