from pydantic import BaseModel


class Budget(BaseModel):
    name: str
    limit: int = 4000
    interval_ms: int = 10000  # 10 seconds


class Param(BaseModel):
    req_id: int = -1
    amount: int = 500
    force: bool = False
    latency: int = 5
    example_ch_count: int = 2950
