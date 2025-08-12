FROM python:3.10
 
WORKDIR /pokemon

COPY . .

RUN pip install -r requirements_dev.txt

RUN pip install -e .

EXPOSE 8000

WORKDIR /pokemon/src/pokemon

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]