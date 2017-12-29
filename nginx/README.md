


# 参考

* [nginx docker hub](https://store.docker.com/images/nginx)
* [nginx alpine](https://github.com/nginxinc/docker-nginx/blob/master/mainline/alpine/Dockerfile)
* [nginx-module-vts](https://github.com/vozlt/nginx-module-vts)




# 下载 update.nginx-module-vts

```bash
cd ./nginx
TAG=v0.1.15
rm -fr nginx-module-vts*
wget -O- https://github.com/vozlt/nginx-module-vts/archive/${TAG}.tar.gz | tar -zx
mv nginx-module-vts* nginx-module-vts

```
