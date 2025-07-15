from fastapi import FastAPI
from routers.es_search_router import router as es_search_router
from routers.dialog_routers import router as dialog_routers

app = FastAPI()
app.include_router(es_search_router)
app.include_router(dialog_routers)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)