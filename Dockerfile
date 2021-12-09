FROM python:3.8.0-slim-buster

WORKDIR /ebook_automation

RUN apt-get update && \
    apt-get -y install gcc git

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY run ./
COPY ./src/ ./src/

ENV OUTDIR=/ebook_automation/output

## replace library version (delete when mutation PR is merged)
RUN git clone -b feature/add-update-cover-cherrypick \
              https://github.com/lb803/thoth-client
RUN rm -rf /usr/local/lib/python3.8/site-packages/thothlibrary/*
RUN mv ./thoth-client/thothlibrary/* \
       /usr/local/lib/python3.8/site-packages/thothlibrary/
##############################################################

ENTRYPOINT ["python3"]

CMD ["python3", "./src/thoth_wrapper.py" "--help"]
