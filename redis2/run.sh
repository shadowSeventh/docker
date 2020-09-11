docker run -p 6379:6379 \
      --name redis \
      -v /Users/lt/work/docker/redis/conf/redis.conf:/etc/redis/redis.conf \
      -v /Users/lt/work/docker/redis/data:/data \
      -d redis redis-server /etc/redis/redis.conf \
      --appendonly yes