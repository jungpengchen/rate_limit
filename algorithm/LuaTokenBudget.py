import threading
from models.Models import Budget, Param
from repositories.Redis import r


class TokenBudget:
    def __init__(self, budget: Budget):
        # Define key names
        self.name = budget.name
        self.r_token_key = budget.name + "_tokens"
        self.r_time_key = budget.name + "_timestamp"
        self.limit = budget.limit
        self.interval_ms = budget.interval_ms
        self.init_update_ms = None
        self.lock = threading.Lock()

        # Use effects replication, not script replication
        # Unclear how to achieve this in Python

    def check_and_eat(self, request_params: Param):
        # should be atomic, lock can be replaced with redis lock
        try:
            with self.lock:
                # print(f'check_and_eat: req{request_params.req_id} enter lock')
                self._check()
                result = self._eat_tokens(request_params)
                # print(f'check_and_eat: req{request_params.req_id} {result} to eat {request_params.amount} end lock')
                return result
        except Exception as e:
            print(str(e))
            print(e.traceback())

    def check_and_release(self, add_tokens):
        # should be atomic, lock can be replaced with redis lock
        try:
            with self.lock:
                # print('check_and_release: enter lock')
                self._check()
                self._release_tokens(add_tokens)
                # print('check_and_release: end lock')
        except Exception as e:
            print(str(e))
            print(e.traceback())

    def _check(self):
        # Get current time
        time_info = r.time()
        self.now_ms = int(time_info[0]) * 1000 + int(time_info[1]) / 1000

        # Get initial token count
        init_tokens = r.get(self.r_token_key)
        # print(f"init_tokens: {init_tokens}, {self.now_ms}")

        if init_tokens is None:
            # If no record found, rewind the clock to refill
            self.prev_tokens = self.limit
            self.last_update_ms = self.now_ms - self.interval_ms
            # print(f"none, {self.prev_tokens} tokens in {self.name}")
        else:
            self.prev_tokens = int(init_tokens)
            self.init_update_ms = r.get(self.r_time_key)

            if self.init_update_ms is None:
                # This is a corruption, need to rewind lastUpdateMS time
                self.last_update_ms = self.now_ms - (self.prev_tokens / self.limit) * self.interval_ms
            else:
                self.last_update_ms = float(self.init_update_ms)
            # print(f"used, {self.prev_tokens} tokens in {self.name}")
        self.gross_tokens = self.prev_tokens
        # print(f'_check: {self.gross_tokens} tokens, {self.now_ms}')

    def _release_tokens(self, add_tokens):
        # Get current time
        time_info = r.time()
        self.now_ms = int(time_info[0]) * 1000 + int(time_info[1]) / 1000
        # Calculate addTokens
        # add_tokens = max(((self.now_ms - self.last_update_ms) / self.interval_ms) * self.limit, 0)
        # Calculate grossTokens
        self.gross_tokens = min(self.prev_tokens + add_tokens, self.limit)
        net_tokens = self.gross_tokens  # Rejection doesn't eat tokens
        # Set valueKey with netTokens
        remain_ms = int(min(self.now_ms - self.last_update_ms, self.interval_ms))
        if remain_ms > 0:
            r.psetex(self.r_token_key, remain_ms, net_tokens)
            # We filled some tokens, so update our timestamp
            r.psetex(self.r_time_key, remain_ms, self.now_ms)
            print(f'_release_tokens: {net_tokens} net_tokens')
        else:
            r.delete(self.r_token_key)
            r.delete(self.r_time_key)

    def _eat_tokens(self, request_param: Param):
        # Calculate netTokens
        net_tokens = self.gross_tokens - request_param.amount

        # Initialize retryDelta
        # retry_delta = 0

        # Initialize flags
        rejected = False

        if net_tokens < 0:  # We used more than we have
            if request_param.force:
                net_tokens = 0  # Drain the swamp
            else:
                rejected = True
                net_tokens = self.gross_tokens  # Rejection doesn't eat tokens
                # todo: add request to queue
                return False

        if not rejected:
            remain_ms = int(min(self.now_ms - self.last_update_ms, self.interval_ms))
            # print(f"{self.now_ms}, remain {remain_ms}")
            # Set valueKey with netTokens
            if remain_ms > 0:
                r.psetex(self.r_token_key, remain_ms, net_tokens)
                if self.init_update_ms is False:
                    # We filled some tokens, so update our timestamp
                    r.psetex(self.r_time_key, remain_ms, self.now_ms)
                else:
                    # We didn't fill any tokens, so just renew the timestamp so it survives with the value
                    r.expire(self.r_time_key, remain_ms)
            else:
                r.delete(self.r_token_key)
                r.delete(self.r_time_key)
        return True

    def __del__(self):
        # print(f'__del__ budget {self.name}')
        with self.lock:
            r.delete(self.r_token_key)
            r.delete(self.r_time_key)
            # print(f'__del__ enter lock, delete {self.r_token_key}')
