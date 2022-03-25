import redis


class RedisManager:
    __instance = None
    host = 'localhost'
    port = 6379

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = redis.Redis(host=cls.host, port=cls.port, decode_responses=True)
        return cls.__instance
