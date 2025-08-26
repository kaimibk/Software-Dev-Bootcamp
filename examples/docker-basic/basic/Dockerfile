FROM debian:11-slim

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    && rm -rf /var/lib/apt/lists/*

COPY foo.txt /bar/foo.txt

CMD ["cat", "/bar/foo.txt"]
