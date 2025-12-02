FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/app/src
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
