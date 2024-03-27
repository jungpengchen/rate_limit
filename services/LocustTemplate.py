from locust import HttpUser, between, task, events
import redis
import time
from test_case.TestCase import llm_functions

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--algo", type=str, env_var="LOCUST_MY_ALGO", default="fixed_window", help="fixed_window/sliding_window/token_budget")

class MyBaseUser(HttpUser):
    wait_time = between(0, 10)
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    host = "http://localhost:8000"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        algo = self.environment.parsed_options.algo
        # algo = 'fixed_window'
        self.endpoint = f"/test/test/{algo}/llm_request/"

    @classmethod
    def setup(cls):
        cls.redis_client.flushall()
    
    def create_param(self, func_index):
        f = llm_functions[func_index]
        req_id = int(time.time())
        amount = f["token_cost"]
        param = f.copy()
        param["req_id"] = req_id
        param["amount"] = amount
        return param
