FROM ghcr.io/home-assistant/base:latest

COPY run.sh /run.sh
RUN chmod a+x /run.sh

LABEL io.hass.type="addon" \
      io.hass.arch="aarch64" \
      org.opencontainers.image.source="https://github.com/AlexMerfy/digital-eye-gateway"

CMD ["/run.sh"]
