FROM ubuntu:18.04
LABEL maintainer="ERplot Analytics <om@prepgo.co.in>"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# 1. Install system dependencies (Legacy Python 2.7 + Modern Python 3)
RUN apt-get update && apt-get install -y \
    python2.7 python-dev python-numpy python-matplotlib \
    python-scipy python-tk python-pip samtools \
    python3 python3-pip python3-dev \
    libgsl-dev libblas-dev liblapack-dev g++ curl \
    libgfortran3 libfreetype6-dev libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Install MISO and Pysam for Analysis Engine (Python 2.7)
RUN python2.7 -m pip install --upgrade pip==18.1 && \
    python2.7 -m pip install pysam==0.15.2 misopy==0.5.4

# 3. Install Streamlit and requirements for GUI (Python 3)
COPY requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# 4. Fix rMATS C-engine library links
RUN ln -s /usr/lib/x86_64-linux-gnu/libgsl.so /usr/lib/libgsl.so.0

# 5. Setup workspace
WORKDIR /app
COPY . /app

# Ensure binaries are executable
RUN chmod +x /app/rMATS-turbo-Linux-UCS4/rMATS_C/rMATSexe

# Expose Streamlit port
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]