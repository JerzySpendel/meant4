
import uuid

import numpy as np
from face_recognition import face_locations
from fastapi import Request
from PIL import Image, ImageDraw

from src.queue import IMAGE_QUEUE
from src.settings import BASE_PATH


def url_for_file(image_filename: str, request: Request) -> str:
    host = request.headers["Host"]
    return f"http://{host}/image/{image_filename}"


async def image_task(image: Image, request: Request):
    uuid_filename = f"{str(uuid.uuid4())}.png"
    processed_image = process_image(image)
    processed_image.save(BASE_PATH / "images" / uuid_filename)

    await IMAGE_QUEUE.put(url_for_file(uuid_filename, request))


def process_image(image: Image) -> Image:
    for location in face_locations(np.array(image)):
        top, right, bottom, left = location

        draw = ImageDraw.Draw(image)
        draw.rectangle([left, top, right, bottom])

    return image
