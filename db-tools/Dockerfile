#
# ---- Base Node ----
FROM python:3.8.0-buster AS base

# Container info
LABEL description="The container to test the DB tools"
LABEL maintainer="Taras Protsenko <easylovv@gmail.com>"

# set working directory
WORKDIR /db-tools

# Install gcc for ujson needs & postgresql-client for test needs
#RUN mkdir -p /usr/share/man/man1 \
#    && mkdir -p /usr/share/man/man7 \
#    && apt-get update \
#    && apt-get upgrade -y \
#    && apt-get install -y gcc postgresql-client \
#    && apt-get autoclean -y


# Copy readme & setup.py
RUN mkdir db_tools
COPY README.md .
COPY setup.py .
# install main requirements
RUN pip install -e . --no-cache-dir
