from rq import Worker, Queue
from app.workers.redis_conn import redis_client

listen = ['transq']

if __name__ == "__main__":
    worker = Worker(list(map(Queue, listen)), connection=redis_client)
    worker.work()

