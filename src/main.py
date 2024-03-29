import asyncio
import contextlib
from io import BytesIO

from fastapi import (BackgroundTasks, FastAPI, Request, UploadFile, WebSocket,
                     WebSocketDisconnect)
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, Response
from PIL import Image, UnidentifiedImageError

from src.processing import image_task
from src.queue import IMAGE_QUEUE
from src.settings import BASE_PATH


class WSManager:
    def __init__(self, queue: asyncio.Queue):
        self.connections: list[WebSocket] = []
        self.queue = queue

    async def connect(self, connection: WebSocket):
        await connection.accept()
        self.connections.append(connection)

    async def disconnect(self, connection: WebSocket):
        self.connections.remove(connection)

    async def broadcast(self):
        while True:
            message = await self.queue.get()

            for connection in self.connections:
                await connection.send_text(message)


@contextlib.asynccontextmanager
async def setup_app(app):
    ws = WSManager(queue=IMAGE_QUEUE)
    app.extra["wsmanager"] = ws
    task_handler = asyncio.create_task(ws.broadcast())
    yield

    task_handler.cancel()


app = FastAPI(lifespan=setup_app)


@app.post("/image")
async def image(file: UploadFile, background_tasks: BackgroundTasks, request: Request):
    try:
        image = Image.open(BytesIO(await file.read()))
        background_tasks.add_task(image_task, image, request)
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400,
            detail={"error": "Input file doesn't seem to be an image file"},
        )

    return Response(status_code=204)


@app.get("/image/{image_filename}")
async def serve_image(image_filename: str):
    path = BASE_PATH / "images" / image_filename
    if not path.exists():
        raise HTTPException(status_code=404, detail={"error": "No such file"})
    return FileResponse(path=BASE_PATH / "images" / image_filename)


@app.websocket("/faces")
async def faces(connection: WebSocket):
    manager: WSManager = app.extra["wsmanager"]
    await manager.connect(connection)
    try:
        while True:
            await connection.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(connection)
