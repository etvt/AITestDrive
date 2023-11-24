FROM python:3.11-bookworm

ARG RUN_AS=user

# build-time user
USER root

# install system dependencies
RUN apt-get update && \
#    apt-get install -y ... && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/* && \
    pip3 install poetry && \
    poetry config virtualenvs.create false && \
    useradd -m user

ADD ./docker/entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin/entrypoint.sh

WORKDIR /app

# install app dependencies
COPY ./pyproject.toml /app/pyproject.toml
RUN poetry install --no-root --no-cache --with dev

# install the project
COPY . /app
RUN poetry install --no-cache --with dev

USER ${RUN_AS}

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
CMD ["python3", "-m", "aitestdrive.main"]
