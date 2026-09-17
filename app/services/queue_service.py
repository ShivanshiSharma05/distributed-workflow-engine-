import json
import redis

from app.db.redis import redis_client


QUEUE_NAME = "workflow_task_queue"


def enqueue_task(task_data: dict):
    message = json.dumps(task_data)
    redis_client.lpush(QUEUE_NAME, message)


def dequeue_task():
    try:
        result = redis_client.brpop(
            QUEUE_NAME,
            timeout=5
        )

        if result is None:
            return None

        _, message = result

        return json.loads(message)

    except redis.exceptions.TimeoutError:
        return None


def get_queue_length():
    return redis_client.llen(QUEUE_NAME)