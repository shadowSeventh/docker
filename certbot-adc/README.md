# certbot-adc

Certbot-**A**uto-**D**ns-**C**hallenge using [certbot](https://certbot.eff.org/)'s
[`--manual-auth-hook`](https://certbot.eff.org/docs/using.html#manual)
and DNS provider's API to add DNS TXT record, get https cert automatically 
from [Let's Encrypt](https://letsencrypt.org/). 
There's no need for a web server or public internet IP address. 
Extremely useful for intranet only https servers.

<!--
## Why this tool?

ACME defined several Identifier Validation Challenges:

- HTTP Challenge: 
    Requires public IP address and a http server.

- TLS with Server Name Indication (TLS SNI) Challenge. 
    Requires public IP address and a special https server.

- DNS Challenge:
    Requires no public IP address, can be used to require a https cert used in intranet only.
    Can be verified by manual or by shell hooks (with DNS provider's API).

- Out-of-Band Challenge:
    Requires human operations.
-->

## Supported DNS providers

-  [aliyun.com](https://wanwang.aliyun.com/domain/dns/)




# How to use

## Setup

```bash
# register a domain, and get the API key/secret for shell hooks.

# prepare enviroment
mkdir -p /data0/store/soft/certbot/docker
mkdir -p /data0/store/soft/certbot/docker/etc/letsencrypt
mkdir -p /data0/store/soft/certbot/docker/var/lib/letsencrypt
mkdir -p /data0/store/soft/certbot/docker/var/log/letsencrypt

# create cerbot-adc config file
cat > /data0/store/soft/certbot/docker/etc/letsencrypt/certbot_adc.yaml <<EOF
providers:
  xxxUniqueConfName:
    type:             aliyun
    keyId:            xxxxxxxxxxxxxxxx
    keySecret:        yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
    region:           cn-hangzhou
    domains:
      - kingsilk.xyz
      - kingsilk.link

EOF

# re-create docker container.
docker stop my-certbot-adc
docker rm my-certbot-adc
docker \
    create  \
    --name my-certbot-adc \
    --entrypoint "/bin/sh" \
    -t \
    -v /data0/store/soft/certbot/docker/etc/letsencrypt:/etc/letsencrypt \
    -v /data0/store/soft/certbot/docker/var/lib/letsencrypt:/var/lib/letsencrypt \
    -v /data0/store/soft/certbot/docker/var/log/letsencrypt:/var/log/letsencrypt \
    btpka3/certbot-adc

# start docker container
docker start my-certbot-adc

# init certbot account (Only once)
docker exec my-certbot-adc \
    certbot \
        register \
        -n \
        --email admin@kingsilk.net \
        --eff-email \
        --agree-tos

# get certs (Only once for each domain )
# For testing, using `--dry-run` option
# If have lot's of subdomain, please combine them in a cert because of the 'Rate Limits'
# If combine multiple subdomain, you can use `--cert-name` to use a specified cert file name
docker exec my-certbot-adc \
    certbot \
        certonly \
        -n \
        --manual \
        --manual-public-ip-logging-ok \
        --manual-auth-hook /usr/local/bin/certbot-adc-manual-auth-hook \
        --manual-cleanup-hook /usr/local/bin/certbot-adc-manual-cleanup-hook \
        --deploy-hook /tmp/a.sh \
        --preferred-challenges dns \
        -d test01.kingsilk.link \
        -d test02.kingsilk.link


# renew
# For testing, using `--dry-run` option
docker exec my-certbot-adc certbot \
    renew \
    -n

# stop docker container
docker stop my-certbot-adc
```

### Cron renew


1. create cron shell `certbot-adc-cron.sh`. 
 
    ```sh
    #!/bin/bash
    docker start my-certbot-adc
    docker exec my-certbot-adc certbot renew -n
    docker stop my-certbot-adc
    ```

1. setup cron jobs

    ```sh
    crontab -e 
    # min   hour    day     month   weekday command
      0     2       *       *       *       /path/to/certbot-adc-cron.sh
    ```


## Developing

```bash
# delete and rebuild locate docker images 
docker stop my-certbot-adc
docker rm my-certbot-adc
docker rmi btpka3/certbot-adc:latest
docker build -t btpka3/certbot-adc .


# same as user's setup step, but using `--dry-run` to test shell hook and renew
docker exec my-certbot-adc \
    certbot \
        certonly \
        --dryrun \
        -n \
        --manual \
        --manual-public-ip-logging-ok \
        --manual-auth-hook /usr/local/bin/certbot-adc-manual-auth-hook \
        --manual-cleanup-hook /usr/local/bin/certbot-adc-manual-cleanup-hook \
        --preferred-challenges dns \
        -d test12.kingsilk.xyz

docker exec my-certbot-adc \
    certbot \
        renew \
        --dryrun \
        -n
```

# References

- Let's Encrypt 
    - [ACME Protocol](https://ietf-wg-acme.github.io/acme/draft-ietf-acme-acme.html)
    - [FAQ: Will Let's Encrypt issue wildcard certificates?](https://certbot.eff.org/faq/#will-let-s-encrypt-issue-wildcard-certificates)
    - [Rate Limits](https://letsencrypt.org/docs/rate-limits/)
    - [Revoking certificates](https://letsencrypt.org/docs/revoking/)
    - [certbot@docker hub](https://hub.docker.com/r/certbot/certbot/)
    - [certbot hooks](https://certbot.eff.org/docs/using.html#pre-and-post-validation-hooks)
- DNS providers
    - aliyun
        - [阿里云-云解析-API](https://help.aliyun.com/document_detail/29740.html)
        - [aliyun python SDK - quick start](https://help.aliyun.com/document_detail/53090.html)
        - [PyPI - aliyun-python-sdk-alidns](https://pypi.python.org/pypi/aliyun-python-sdk-alidns)
        - [Github - aliyun-python-sdk-alidns](https://github.com/aliyun/aliyun-openapi-python-sdk/tree/master/aliyun-python-sdk-alidns)
    - tencent cloud
        - [腾讯-云解析-API](https://cloud.tencent.com/document/api/302/8516)
        - [Github - qcloudapi-sdk-python](https://github.com/QcloudApi/qcloudapi-sdk-python)
        - [PyPI - qcloudapi-sdk-python](https://pypi.python.org/pypi/qcloudapi-sdk-python/2.0.9)
    - DNSPod
        - [DNSPod用户API文档](https://www.dnspod.cn/docs/index.html)
    - GoDaddy
        - [API](https://developer.godaddy.com/doc)
    
- deploy-hook
    - aliyun CDN
        - [SetDomainServerCertificate - 设置证书](https://help.aliyun.com/document_detail/45014.html)
