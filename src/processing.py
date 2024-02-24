import asyncio
from fastapi import UploadFile

from src.queue import IMAGE_QUEUE


async def process_image(file: UploadFile):
    await asyncio.sleep(1)
    print('Done!')