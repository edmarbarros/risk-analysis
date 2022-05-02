import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from risk_analysis_api import risk_analysis_controller

app = FastAPI()
app.include_router(risk_analysis_controller.router)


@app.get("/health")
async def root():
    return {"status": "ok", "info": {}, "error": {}, "details": {}}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Origin - Risk Analysis",
        version="0.1.0",
        description="Origin Risk Analysis OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
