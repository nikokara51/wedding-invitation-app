FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
# ensure DB schema (on first run)
RUN python -c "import app.database; print('db-init-ok')"
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
