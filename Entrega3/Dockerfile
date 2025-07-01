FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV HADOOP_VERSION=3.3.6
ENV PIG_VERSION=0.17.0
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV PIG_HOME=/opt/pig
ENV PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PIG_HOME/bin

# Instalar todo lo necesario
RUN apt-get update && apt-get install -y \
    wget curl gnupg lsb-release software-properties-common \
    openjdk-11-jdk \
    python3.10 python3.10-distutils python3.10-venv python3-pip \
    ssh net-tools unzip vim ca-certificates \
    && ln -sf /usr/bin/python3.10 /usr/bin/python3 \
    && ln -sf /usr/bin/pip3 /usr/bin/pip \
    && apt-get clean

WORKDIR /app
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz -C /opt && \
    mv /opt/hadoop-${HADOOP_VERSION} /opt/hadoop && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# Instalar Pig
RUN wget https://downloads.apache.org/pig/pig-${PIG_VERSION}/pig-${PIG_VERSION}.tar.gz && \
    tar -xzf pig-${PIG_VERSION}.tar.gz -C /opt && \
    mv /opt/pig-${PIG_VERSION} /opt/pig && \
    rm pig-${PIG_VERSION}.tar.gz

# Crear usuario y directorio de trabajo

RUN chmod +x start.sh  


# Verificar versiones
RUN hadoop version && pig -version && python3 --version

CMD [ "./start.sh" ]