llm_functions = [
    {
        "event_name": "quiz_generator_history",
        "latency": 10,
        "token_cost": 200,
        "example_ch_count": 1125
    },
    {
        "event_name": "quiz_generator_math",
        "latency": 60,
        "token_cost": 1000,
        "example_ch_count": 5990
    },
    {
        "event_name": "lesson_summary",
        "latency": 20,
        "token_cost": 500,
        "example_ch_count": 2950
    }
]

# api_keys = [
#     {
#         "deployment": "production_1",
#         "rate_limit": 4000
#     },
#     {
#         "deployment": "production_2",
#         "rate_limit": 8000
#     }
# ]

api_keys = [
    {
        "deployment": "large",
        "rate_limit": 100000
    },
    {
        "deployment": "small",
        "rate_limit": 10000
    }
]