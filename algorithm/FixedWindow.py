import time
import threading
import redis
import os
from models.Models import Budget, Param
from repositories.Redis import r


class FixedWindowCounter:
    def __init__(self, budget: Budget) -> None:
        assert isinstance(r, redis.Redis)
        self.db = r
        self.interval_ms = budget.interval_ms
        self.lock = threading.Lock()
        self.name = budget.name
        self.r_token_key = budget.name + "_fixwindow"
        self.limit = budget.limit

    def check_and_eat(self, request_params: Param):
        # should be atomic, lock can be replaced with redis lock
        try:
            with self.lock:
                # print(f'check_and_eat: req{request_params.req_id} enter lock')
                result = self._increment(request_params.amount)
                # print(f'check_and_eat: req{request_params.req_id} {result} to eat {request_params.amount} end lock')
                return result
        except Exception as e:
            print(str(e))
            print(e.traceback())

    def _get_current_bucket_and_ttl(self):
        time_info = self.db.time()
        now_ms = int(time_info[0]) * 1000 + int(time_info[1]) / 1000
        time_bucket = now_ms // (self.interval_ms)
        ttl_ms = int(self.interval_ms - (now_ms % self.interval_ms))
        return f"{self.r_token_key}_{time_bucket}", ttl_ms  # insert user id here

    def _increment(self, value: int) -> bool:
        key, ttl = self._get_current_bucket_and_ttl()
        token_cost = self._get_count(key)
        if token_cost >= self.limit:
            return False
        elif token_cost == 0:
            # first request in budget
            self.db.psetex(key, ttl, value)
        else:
            self.db.incrby(key, value)
        return True

    def _get_count(self, key) -> int:
        cnt = self.db.get(key)
        if cnt is None:  # redis return None on key not found
            return 0
        return int(cnt)
