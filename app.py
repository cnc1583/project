import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from back.components.naver_api.router import router as trend_router
from back.components.kis_api.router import router as stock_router
from back.components.real_estate_api.router import router as real_estate_router
from back.presentation.article_router import router as article_router

def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(trend_router, tags=["Trend"])
    app.include_router(stock_router, tags=["Stock"])
    app.include_router(real_estate_router, tags=["RealEstate"])
    app.include_router(article_router, tags=["Article"])

    app.mount("/", StaticFiles(directory=os.path.join("frontend", "build"), html=True), name="frontend")

    return app