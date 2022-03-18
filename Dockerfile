FROM python:3.8.0-slim-buster

WORKDIR /ebook_automation

RUN apt-get update && \
    apt-get -y install gcc

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY run ./
COPY ./src/ ./src/

ENV OUTDIR=/ebook_automation/output

ENTRYPOINT ["python3"]

CMD ["python3", "./src/thoth_wrapper.py" "--help"]
