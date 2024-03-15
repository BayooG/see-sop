import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from service.endpoints.root import router as root_router
from service.endpoints.mvp import router as mvp_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(root_router)
app.include_router(mvp_router)

# Add middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://relaxed-mermaid-46cc2b.netlify.app",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TODO: remove this when in production
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
