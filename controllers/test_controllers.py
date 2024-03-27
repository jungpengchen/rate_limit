from fastapi import APIRouter, Request
import asyncio
from repositories.Redis import close_connection
from algorithm.LuaTokenBudget import Param, Budget, TokenBudget
from algorithm.SlidingWindow import SlidingWindow
from algorithm.FixedWindow import FixedWindowCounter
from services.Chat import invoke
from test_case.TestCase import api_keys

router = APIRouter(prefix="/test", tags=["Test"])
# router = APIRouter(prefix="/api/v1/lexi-quiz/test", tags=["Test"])
budget_models = [Budget(name=k["deployment"], limit=k["rate_limit"], interval_ms=60000) for k in api_keys]
budgets = [TokenBudget(m) for m in budget_models]
counters = [FixedWindowCounter(m) for m in budget_models]


@router.post("/test/token_budget/llm_request/")
async def test_request_token_budget(param: Param):
    for b in budgets:
        if b.check_and_eat(param):
            invoke(b.name, param)
            await asyncio.sleep(param.latency)  # lantency
            b.check_and_release(param.amount)
            return "success"
    return 429, "failed"


@router.post("/test/fixed_window/llm_request/")
async def test_request_fixed_window(param: Param):
    # total_sleep = 0
    for c in counters:
        if c.check_and_eat(param):
            # print(req_id,"OK",c.name)
            invoke(c.name, param)
            await asyncio.sleep(param.latency)  # lantency
            return "success"
        # else:
        #     print(req_id,"Failed",b.name)
        # random_sleep_i = (random.randint(0,5))/10
        # time.sleep(random_sleep_i)
        # total_sleep += random_sleep_i
    return 500, "failed"


@router.post("/test/sliding_window/llm_request/")
async def test_request_sliding_window(param: Param):
    event_name = param.req_id
    token_cost = param.amount
    latency = param.latency
    sw = SlidingWindow()
    for b in budget_models:
        # print(j)
        event_name = b.name + "_event"
        token_limit = int(b.limit)
        # print(j,token_limit)

        if sw.is_request_allowed(event_name, token_limit):
            invoke(b.name, param)
            sw.add_request(event_name, token_cost)
            return "success"
    return 500, "failed"


@router.on_event("shutdown")
async def shutdown_event():
    close_connection()
    exit()
