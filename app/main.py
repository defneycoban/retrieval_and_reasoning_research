from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="A multilingual RAG platform for retrieval and reasoning experiments.",
    version="0.1.0",
)
app.include_router(router, prefix="/api")
app.mount("/static", StaticFiles(directory="app/web"), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse("app/web/index.html")


@app.head("/", include_in_schema=False)
def head_index() -> None:
    return None
