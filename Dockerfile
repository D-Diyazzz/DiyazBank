FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN apk add build-base

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --upgrade -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:$PWD"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
