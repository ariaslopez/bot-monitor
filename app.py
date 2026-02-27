"""
Bot Monitor Dashboard

FastAPI server con métricas en tiempo real de Twitter.
"""

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import uvicorn

from api.twitter import TwitterClient
from api.metrics import MetricsCollector
from api.status import StatusChecker

load_dotenv()

# Inicializar FastAPI
app = FastAPI(
    title="Bot Monitor",
    description="Dashboard de monitoreo para bots de Twitter",
    version="1.0.0"
)

# Static files y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Inicializar clientes
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
if not bearer_token:
    print("⚠️  WARNING: TWITTER_BEARER_TOKEN no configurado en .env")

twitter_client = TwitterClient(bearer_token) if bearer_token else None
metrics_collector = MetricsCollector(twitter_client) if twitter_client else None
status_checker = StatusChecker(twitter_client) if twitter_client else None


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Página principal del dashboard.
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get("/api/bots")
async def get_bots():
    """
    Obtiene lista de bots con sus métricas.
    """
    if not metrics_collector:
        return JSONResponse(
            status_code=503,
            content={"error": "Twitter API no configurado"}
        )
    
    try:
        bots_data = await metrics_collector.get_all_bots_metrics()
        return JSONResponse(content=bots_data)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.get("/api/bot/{handle}")
async def get_bot_metrics(handle: str):
    """
    Obtiene métricas de un bot específico.
    """
    if not metrics_collector:
        return JSONResponse(
            status_code=503,
            content={"error": "Twitter API no configurado"}
        )
    
    try:
        metrics = await metrics_collector.get_bot_metrics(handle)
        return JSONResponse(content=metrics)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.get("/api/status")
async def get_status():
    """
    Obtiene status general del sistema.
    """
    if not status_checker:
        return JSONResponse(
            status_code=503,
            content={"error": "Twitter API no configurado"}
        )
    
    try:
        status = await status_checker.get_system_status()
        return JSONResponse(content=status)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "version": "1.0.0"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "True") == "True"
    
    print(f"🚀 Bot Monitor Dashboard")
    print(f"🌐 http://{host}:{port}")
    print("")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=debug
    )
