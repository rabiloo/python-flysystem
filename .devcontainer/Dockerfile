# syntax=docker.io/docker/dockerfile:1.4

ARG VARIANT=3.10
FROM python:${VARIANT} AS runtime

# Update PIP
RUN pip install --upgrade pip

# Create the user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=${USER_UID}
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -s /bin/bash -m ${USERNAME} \
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# Create workspace
ARG WORKSPACE=/workspace
RUN mkdir -p ${WORKSPACE} \
    && chown -R ${USER_UID}:${USER_GID} ${WORKSPACE}

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# Change user and workspace
USER ${USERNAME}
WORKDIR ${WORKSPACE}

# RUN export PATH=/home/vscode/.local/bin:$$PATH
# RUN pip install black flake8 pytest

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp
