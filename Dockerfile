FROM python:3.11
WORKDIR /app
COPY requirments.txt .
RUN pip install --no-cache-dir  --upgrade -r requirments.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]