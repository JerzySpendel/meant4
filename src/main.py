from io import BytesIO
import typing
from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.exceptions import HTTPException
from PIL import Image, UnidentifiedImageError

from src.processing import process_image

app = FastAPI()

@app.post('/image')
async def image(file: UploadFile, background_tasks: BackgroundTasks):
    try:
        Image.open(BytesIO(await file.read()))
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail={'error': 'Input file doesn\'t seem to be an image file'})

    background_tasks.add_task(process_image, file)
    return {'size': file}