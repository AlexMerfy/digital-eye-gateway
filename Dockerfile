FROM ghcr.io/home-assistant/base:latest

RUN apk add --no-cache python3 py3-pip \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir \
        firebase-admin \
        flask \
        gunicorn

ENV PATH="/opt/venv/bin:$PATH"

COPY gateway.py /app/gateway.py
COPY run.sh /run.sh

RUN chmod a+x /run.sh

WORKDIR /app

LABEL io.hass.type="addon" \
      io.hass.arch="aarch64" \
      org.opencontainers.image.source="https://github.com/AlexMerfy/digital-eye-gateway"

CMD ["/run.sh"]
