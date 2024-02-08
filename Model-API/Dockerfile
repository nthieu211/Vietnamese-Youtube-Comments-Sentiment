FROM python:3.11.7-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /code

COPY requirements.txt ./

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    openjdk-17-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64

RUN pip install git+https://github.com/facebookresearch/fastText.git

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install torch==2.1.2 --index-url https://download.pytorch.org/whl/cpu

COPY . .

RUN python -m pypyr pipelines/sentiment-model-download