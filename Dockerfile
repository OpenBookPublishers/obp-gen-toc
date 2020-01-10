FROM python:3.8.0-slim-buster

WORKDIR /ebook_automation

RUN apt-get update && \
    apt-get -y install gcc mupdf-tools

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY run ./
COPY ./src/ ./src/

ENV OUTDIR=/ebook_automation/output

CMD bash run file