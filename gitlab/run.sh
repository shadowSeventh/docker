# 通过docker run中加入环境变量,取名为gitlab
docker run --detach \       # 后台运行 -d
    --hostname nas.seventh.party \  # 指定容器域名,未知功能:创建镜像仓库的时候使用到
    -p 10443:443 \           # 将容器内443端口映射到主机8443,提供https服务
    -p 10080:10080 \              # 将容器内80端口映射到主机8080,提供http服务
    -p 10022:10022 \           # 将容器内22端口映射到主机1002,提供ssh服务
    --name gitlab \         # 指定容器名称
    --restart=unless-stopped \                   # 容器运行中退出时（不是手动退出）,自动重启
    --v /Users/lt/docker/gitlab/etc:/etc/gitlab \       # 将本地/var/lib/docker/volumes/gitlab-data/etc挂载到容器内/etc/gitlab
    --v /Users/lt/docker/gitlab/log:/var/log/gitlab \   # 将本地将本地/var/lib/docker/volumes/gitlab-data/log挂载到容器内/var/log/gitlab
    --v /Users/lt/docker/gitlab/data:/var/opt/gitlab \  # 将本地将本地/var/lib/docker/volumes/gitlab-data/data挂载到容器内/var/opt/gitlab
  registry.cn-hangzhou.aliyuncs.com/seventh/gitlab:v0.0.1


docker run --detach  \
    --hostname nas.seventh.party \
    -p 10443:443 \
    -p 10080:10080 \
    -p 10022:10022 \
    --name gitlab \
    --restart=unless-stopped \
    -v /Users/lt/docker/gitlab/etc:/etc/gitlab \
    -v /Users/lt/docker/gitlab/log:/var/log/gitlab \
    -v /Users/lt/docker/gitlab/data:/var/opt/gitlab \
    registry.cn-hangzhou.aliyuncs.com/seventh/gitlab:v0.0.1