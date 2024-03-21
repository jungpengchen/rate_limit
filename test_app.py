print('run test_app')
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from controllers.test_controllers import router as test_router

# app = FastAPI(openapi_url="/docs/lexi-quiz/openapi.json", docs_url="/docs/lexi-quiz")
app = FastAPI(docs_url="/docs")
# TODO: This CORS setting maybe not that well, survey about CORS and set it with reason


app.include_router(test_router)

# * ------------------------Root endpoint------------------------


# * required for fargate task group healthy check
@app.get("/", tags=["Root"])
async def read_root(request: Request):
    return "test"
