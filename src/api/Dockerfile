FROM python:3.10

WORKDIR /app

COPY src/api/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/api/ /app/
COPY src/api/model.pkl /app/model.pkl

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "500"]