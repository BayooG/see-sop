from fastapi import FastAPI
from service.endpoints.root import router as root_router
from service.endpoints.mvp import router as mvp_router

app = FastAPI()

app.include_router(root_router)
app.include_router(mvp_router)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
