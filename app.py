from fastapi import FastAPI
from routers.es_search_router import router as es_search_router

app = FastAPI()
app.include_router(es_search_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)