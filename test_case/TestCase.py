llm_functions = [
    {
        "event_name": "quiz_generator_history",
        "latency": 10,
        "token_cost": 200
    },
    {
        "event_name": "quiz_generator_math",
        "latency": 60,
        "token_cost": 1000
    },
    {
        "event_name": "lesson_summary",
        "latency": 20,
        "token_cost": 500
    }
]

api_keys = [
    {
        "deployment": "production_1",
        "rate_limit": 4000
    },
    {
        "deployment": "production_2",
        "rate_limit": 8000
    }
]