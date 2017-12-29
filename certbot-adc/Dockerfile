FROM certbot/certbot:v0.19.0

COPY . /tmp/certbot_adc
ENV CERTBOT_ADC_YAML=/etc/letsencrypt/certbot_adc.yaml

RUN \
    apk add --no-cache --virtual .build-deps \
        gcc \
        linux-headers \
        openssl-dev \
        musl-dev \
        libffi-dev \
    && pip install /tmp/certbot_adc \
    && apk del .build-deps \
    && rm -fr /tmp/certbot_adc
