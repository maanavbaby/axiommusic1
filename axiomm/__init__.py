# Copyright (c) 2025 AxiomBots
# Licensed under the MIT License.
# This file is part of AxiomXMusic


import time
import asyncio
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=10485760, backupCount=5),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("ntgcalls").setLevel(logging.CRITICAL)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


__version__ = "3.0.3"

from config import Config

config = Config()
config.check()
tasks = []
boot = time.time()

from axiomm.core.bot import Bot
app = Bot()

from axiomm.core.dir import ensure_dirs
ensure_dirs()

from axiomm.core.userbot import Userbot
userbot = Userbot()

from axiomm.core.mongo import MongoDB
db = MongoDB()

from axiomm.core.lang import Language
lang = Language()

from axiomm.core.telegram import Telegram
from axiomm.core.youtube import YouTubeAPI

tg = Telegram()
yt = YouTubeAPI()

from axiomm.helpers import Queue, Thumbnail
queue = Queue()
thumb = Thumbnail()

from axiomm.core.calls import TgCall
axiom = TgCall()


async def stop() -> None:
    logger.info("Stopping...")
    for task in tasks:
        task.cancel()
        try:
            await task
        except asyncio.exceptions.CancelledError:
            pass

    await app.exit()
    await userbot.exit()
    await db.close()
    await thumb.close()

    logger.info("Stopped.\n")
