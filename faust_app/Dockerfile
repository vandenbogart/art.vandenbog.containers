FROM python:3.7-slim
    
RUN apt-get update && apt-get install -y wget && apt-get install -y git

# Dockerize install to wait on kafka tcp connection
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

# RocksDB install
RUN apt-get install -y build-essential libsnappy-dev zlib1g-dev libbz2-dev libgflags-dev liblz4-dev cmake make
RUN git clone https://github.com/facebook/rocksdb.git
WORKDIR /rocksdb/build
RUN cmake ..
RUN make
RUN make install INSTALL_PATH=/usr
WORKDIR /rocksdb
RUN export CPLUS_INCLUDE_PATH=${CPLUS_INCLUDE_PATH}${CPLUS_INCLUDE_PATH:+:}`pwd`/include/
RUN export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}${LD_LIBRARY_PATH:+:}`pwd`/build/
RUN export LIBRARY_PATH=${LIBRARY_PATH}${LIBRARY_PATH:+:}`pwd`/build/
RUN pip3 install "Cython>=0.20"
RUN pip3 install python-rocksdb

# setup.py install
WORKDIR /app
COPY setup.py /app
RUN python3 setup.py develop

# add source code
COPY . /app

ENTRYPOINT dockerize -wait tcp://kafka:9092 -timeout 60s faust_app worker -l info
