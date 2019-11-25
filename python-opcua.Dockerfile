FROM python
WORKDIR /usr/opc/src


RUN apt-get update && apt-get install -y \
    zsh \
    wget \
    git

COPY python-requirements.txt ./
RUN pip install --no-cache-dir -r python-requirements.txt

RUN git clone https://github.com/linsjb/Config-files.git ~/.dotfile_configs
RUN sh ~/.dotfile_configs/build_config.sh
