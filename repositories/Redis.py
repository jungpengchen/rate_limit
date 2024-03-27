import redis
import os

# Set the PYTHONIOENCODING environment variable to UTF-8
os.environ['PYTHONIOENCODING'] = 'UTF-8'

# Connect to Redis server
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def check_redis_connection():
    try:
        # Replace 'localhost' and 6379 with your Redis host and port
        r.ping()  # This will raise an exception if the connection fails
        print("Redis connection successful.")
    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")


# Call the function to check the Redis connection
check_redis_connection()


def close_connection():
    r.close()