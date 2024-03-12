from fastapi import FastAPI
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


@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
