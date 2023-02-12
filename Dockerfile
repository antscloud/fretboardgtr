
FROM python:3.10-bullseye

LABEL description="fretboardgtr docker image"

RUN apt-get update \
    && apt-get install -y --no-install-recommends libudunits2-dev gdb \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY . /fretboardgtr/

RUN pip install /fretboardgtr[dev]
