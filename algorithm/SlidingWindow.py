import time
from test_case.TestCase import api_keys
from repositories.Redis import r

api_keys_list = [i["deployment"] for i in api_keys]
for i in api_keys:
    r.hset(i['deployment'], key=i["deployment"], value=i["rate_limit"], mapping=i)
import uuid

window_seconds = 60


def generate_request_id(event_name):
    return f"{event_name}:{uuid.uuid4()}"


class SlidingWindow:
    def add_request(event_name, token_cost, latency=60):
        current_time = time.time()
        request_id = generate_request_id(event_name)

        r.zadd(event_name, {request_id: current_time})

        r.set(f"request_details:{request_id}", value=token_cost, ex=latency + window_seconds)

        return request_id, current_time

    def is_request_allowed(event_name, token_limit=3000):
        min_timestamp = time.time() - 60  # 過去 60 秒

        r.zremrangebyscore(event_name, '-inf', min_timestamp)
        # print("??")

        request_ids = r.zrangebyscore(event_name, min_timestamp, 'inf')

        total_tokens = 0
        for req_id in request_ids:

            token_cost = r.get(f"request_details:{req_id.decode('utf-8')}")
            if token_cost is None:
                continue
            total_tokens += int(token_cost)

        return total_tokens <= token_limit
