"""
The RedisManager class manages the connection to a Redis server.

This class provides a simple interface for creating and accessing a Redis client
using a connection pool.

Attributes:
    redis_pool (redis.ConnectionPool): The connection pool for Redis.
    
Methods:
    - __init__: Initializes the connection pool with configuration settings from the Config object.
    - get_client: Returns a Redis client using the established connection pool.
"""

import redis
from config import Config


class RedisManager:
    def __init__(self):
        """
        Initializes the connection pool for Redis.

        It takes configuration parameters from the Config object to create a connection pool
        for Redis, allowing efficient and reusable connections.
        """
        self.redis_pool = redis.ConnectionPool(
            host=Config.CACHE_REDIS_HOST,
            port=Config.CACHE_REDIS_PORT,
            db=Config.CACHE_REDIS_DB,
        )

    def get_client(self):
        """
        Returns a Redis client using the established connection pool.

        This method provides access to a Redis client that uses the connection pool
        for efficient Redis operations.
        """
        return redis.StrictRedis(connection_pool=self.redis_pool)
