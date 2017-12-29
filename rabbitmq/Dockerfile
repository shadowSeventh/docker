FROM rabbitmq:3.6.10-alpine

COPY env.sh /etc/profile.d/

# 启用 bash
RUN \
    apk add --no-cache bash shadow tzdata \
    && usermod -s /bin/bash root \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone

# 因为 /var/lib/rabbitmq 是一个 data VOLUME，造成 .bashrc 无法生成
#&& echo ". /etc/profile" > /var/lib/rabbitmq/.bashrc


EXPOSE      \
    4369    \
    5671    \
    5672    \
    25672   \
    15671   \
    15672   \
    1883    \
    8883    \
    15675


