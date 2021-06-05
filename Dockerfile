FROM alpine:3

MAINTAINER PufferOverflow

RUN apk add --no-cache git py3-pip build-base python3-dev &&\
    git clone --depth 1 --branch master --single-branch https://github.com/PufferOverfIow/CyberPuffer.git /var/bot &&\
    pip install --no-cache-dir wheel &&\
    pip install --no-cache-dir -r /var/bot/requirements.txt &&\
    pip uninstall -y wheel &&\
    apk del build-base python3-dev git

WORKDIR /var/bot
CMD ["/var/bot/bot.py"]
ENTRYPOINT ["python3"]