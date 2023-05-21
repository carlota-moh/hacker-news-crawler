FROM tiangolo/uvicorn-gunicorn:python3.10
WORKDIR /api
COPY . /api
RUN pip install --upgrade -r requirements.txt
RUN pip install psycopg2-binary
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]