FROM python:3.10
 
WORKDIR /journal

COPY . .

RUN pip install -r requirements_dev.txt

RUN pip install -e .

EXPOSE 8001

WORKDIR /journal/src/journal

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]