import os
from dotenv import load_dotenv
import logging
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

# 1) Загрузим .env
load_dotenv()

# 2) Настроим логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("notification-service")

# 3) Импорт consumer после того, как env загружен
from .rabbit import consume

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Этот блок выполняется при старте
    logger.info("Notification service is starting…")
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, consume)
    yield
    # Этот блок (если нужен) — при завершении приложения:
    logger.info("Notification service is shutting down…")

app = FastAPI(title="Notification Service", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}
