from fastapi import APIRouter, Request
import asyncio
from algorithm.LuaTokenBudget import Param, Budget, TokenBudget, close_connection
from test_case.TestCase import api_keys

router = APIRouter(prefix="/test", tags=["Test"])
# router = APIRouter(prefix="/api/v1/lexi-quiz/test", tags=["Test"])
budget_models = [Budget(name=k["deployment"], limit=k["rate_limit"], interval_ms=60000) for k in api_keys]
budgets = [TokenBudget(m) for m in budget_models]


@router.post("/test/token_budget/llm_request/")
async def test_request_token_budget(param: Param):
    for b in budgets:
        if b.check_and_eat(param):
            await asyncio.sleep(param.latency)  # lantency
            b.check_and_release(param.amount)
            return "success"
    return 500, "failed"


@router.post("/test/fixed_window/llm_request/")
async def test_request_fixed_window(param: Param):
    for b in budgets:
        if b.check_and_eat(param):
            await asyncio.sleep(param.latency)  # lantency
            b.check_and_release(param.amount)
            return "success"
    return 500, "failed"


@router.post("/test/sliding_window/llm_request/")
async def test_request_sliding_window(param: Param):
    for b in budgets:
        if b.check_and_eat(param):
            await asyncio.sleep(param.latency)  # lantency
            b.check_and_release(param.amount)
            return "success"
    return 500, "failed"


@router.on_event("shutdown")
async def shutdown_event():
    close_connection()
    exit()
