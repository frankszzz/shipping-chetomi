FROM python:3.11-slim

ARG ORS_API_KEY
ARG SECRET_KEY

ENV ORS_API_KEY=${ORS_API_KEY}
ENV SECRET_KEY=${SECRET_KEY}
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p instance

EXPOSE 4010

CMD python seed_data.py && gunicorn --bind 0.0.0.0:4010 app:app
