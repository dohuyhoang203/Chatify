import redis

pool = redis.ConnectionPool.from_url("redis://:@163.124.2.102:6379/")


class BaseRedis:

    prefix_key = ""

    def get_data(self, key):
        r = redis.Redis(connection_pool=pool, decode_responses=True)
        final_key = "{prefix}#{key}".format(prefix=self.prefix_key, key=key)
        return r.get(final_key)

    def set_data(self, key, value, ex=0):
        r = redis.Redis(connection_pool=pool, decode_responses=True)
        final_key = "{prefix}#{key}".format(prefix=self.prefix_key, key=key)
        if ex:
            return r.set(final_key, value, ex=ex)
        return r.set(final_key, value)

    def del_data(self, keys):
        r = redis.Redis(connection_pool=pool, decode_responses=True)
        final_keys = list()
        for key in keys:
            final_key = "{prefix}#{key}".format(prefix=self.prefix_key, key=key)
            final_keys.append(final_key)
        return r.delete(*final_keys)

    def hset_data(self, key, field, value):
        r = redis.Redis(connection_pool=pool, decode_responses=True)
        final_key = "{prefix}#{key}".format(prefix=self.prefix_key, key=key)
        return r.hset(final_key, field, value)

    def hmset_data(self, key, field, value):
        r = redis.Redis(connection_pool=pool, decode_responses=True)
        final_key = "{prefix}#{key}".format(prefix=self.prefix_key, key=key)
        return r.hmset(final_key, field, value)

    def hvals(self, key):
        r = redis.Redis(connection_pool=pool, decode_responses=True)
        final_key = "{prefix}#{key}".format(prefix=self.prefix_key, key=key)
        return r.hvals(final_key)

    def hgetall(self, key):
        r = redis.Redis(connection_pool=pool, decode_responses=True)
        final_key = "{prefix}#{key}".format(prefix=self.prefix_key, key=key)
        return r.hgetall(final_key)

    def hdel_data(self, key, field):
        r = redis.Redis(connection_pool=pool, decode_responses=True)
        final_key = "{prefix}#{key}".format(prefix=self.prefix_key, key=key)
        return r.hdel(final_key, field)

    def hget_data(self, key, field):
        r = redis.Redis(connection_pool=pool, decode_responses=True)
        final_key = "{prefix}#{key}".format(prefix=self.prefix_key, key=key)
        return r.hget(final_key, field)

    def hkeys(self, key):
        r = redis.Redis(connection_pool=pool)
        final_key = "{prefix}#{key}".format(prefix=self.prefix_key, key=key)
        return r.hkeys(final_key)

    def hdel_all_data(self, key):
        r = redis.Redis(connection_pool=pool, decode_responses=True)
        final_key = "{prefix}#{key}".format(prefix=self.prefix_key, key=key)
        field = r.hkeys(final_key)
        return r.hdel(final_key, field)
