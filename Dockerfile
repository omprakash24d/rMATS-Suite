FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install system dependencies
RUN apt-get update && apt-get install -y \
    python2.7 python-dev python-numpy python-matplotlib \
    python-scipy python-tk python-pip samtools \
    libgsl-dev libblas-dev liblapack-dev g++ curl \
    libgfortran3 libfreetype6-dev libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Install MISO and Pysam
RUN pip install pysam==0.15.2 misopy==0.5.4

# 3. CRITICAL FIX: Create the path the script is hard-coded to look for
# We find where pip installed misopy and link it to /opt/MISO/misopy
RUN mkdir -p /opt/MISO && \
    MISOPATH=$(python -c "import misopy; import os; print(os.path.dirname(misopy.__file__))") && \
    ln -s $MISOPATH /opt/MISO/misopy

# 4. Fix rMATS C-engine library links
RUN ln -s /usr/lib/x86_64-linux-gnu/libgsl.so /usr/lib/libgsl.so.0
RUN ln -sf /usr/bin/python2.7 /usr/bin/python

# 5. Copy your local rMATS and Sashimi folders
WORKDIR /opt
COPY ./rMATS-turbo-Linux-UCS4 /opt/rmats
COPY ./rmats2sashimiplot /opt/sashimi

ENV PATH="/opt/rmats:/opt/sashimi:${PATH}"
WORKDIR /data