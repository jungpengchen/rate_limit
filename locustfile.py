from locust import HttpUser, between, task, events
import redis
import time
from test_case.TestCase import llm_functions
from services import LocustTemplate

class User1(LocustTemplate.MyBaseUser):
    @task
    def my_task(self):
        # Your task here for User1
        param = self.create_param(0)
        self.client.post(self.endpoint, json=param)

class User2(LocustTemplate.MyBaseUser):
    @task
    def my_task(self):
        # Your task here for User2
        param = self.create_param(1)
        self.client.post(self.endpoint, json=param)

class User3(LocustTemplate.MyBaseUser):
    @task
    def my_task(self):
        # Your task here for User3
        param = self.create_param(2)
        self.client.post(self.endpoint, json=param)

