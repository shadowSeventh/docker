FROM mysql:5.7

COPY env.sh /etc/profile.d/

# 启用 bash
RUN \
    apk add --no-cache bash shadow tzdata \
    && usermod -s /bin/bash root \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && echo ". /etc/profile" > /root/.bashrc

CMD ["/bin/bash"]


