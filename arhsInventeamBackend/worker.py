import os
import redis
from redis import Redis
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker


listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL')
if not redis_url:
    raise RuntimeError("Set up Heroku Data For Redis first, \
    make sure its config var is named 'REDIS_URL'.")

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()




