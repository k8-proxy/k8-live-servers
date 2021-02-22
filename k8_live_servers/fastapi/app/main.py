from fastapi                             import FastAPI
from mangum                              import Mangum
from k8_live_servers.fastapi.app.api.api import router

app = FastAPI(root_path="/Prod")


@app.get("/")
async def root():
    return {"message": "Welcome to Screenshot FastAPI"}


app.include_router(router, prefix="/api/v1")
handler = Mangum(app)