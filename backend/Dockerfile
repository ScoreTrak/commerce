FROM ubuntu:focal

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PIPENV_VENV_IN_PROJECT 1
ENV PATH /opt/app/.venv/bin:$PATH

WORKDIR /opt/app

ARG UNAME=django
ARG UID=1234
ARG GID=1234

RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID  -s /bin/bash $UNAME && chown $UNAME:$UNAME /opt/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc make python3 python3-dev python3-pip python3-setuptools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --trusted-host pypi.python.org pipenv

USER $UNAME

COPY --chown=$UNAME:$UNAME Pipfile Pipfile.lock ./
RUN pipenv install --ignore-pipfile

COPY --chown=$UNAME:$UNAME . .

RUN mkdir static; ./manage.py collectstatic

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "ldfinance.asgi:application"]
