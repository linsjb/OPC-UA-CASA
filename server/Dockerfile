FROM python
WORKDIR /usr/opc/src

RUN apt-get update && apt-get install -y zsh

#COPY python-requirements-server.txt ./
#RUN pip install --no-cache-dir -r python-requirements-server.txt
RUN pip install asyncua pyyaml

RUN git clone https://github.com/linsjb/Config-files.git ~/.dotfile_configs
RUN sh ~/.dotfile_configs/build_config.sh
