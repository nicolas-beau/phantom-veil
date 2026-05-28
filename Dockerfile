FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY phantom_veil/ phantom_veil/
COPY config/ config/

ENV PHANTOM_CONFIG=/app/config/phantom-veil.yaml
ENV PYTHONPATH=/app

EXPOSE 9090

CMD ["python", "-m", "phantom_veil.server"]
