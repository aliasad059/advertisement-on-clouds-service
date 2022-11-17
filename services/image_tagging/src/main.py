import uvicorn
from fastapi import FastAPI, Form, UploadFile, File
from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn.config import LOGGING_CONFIG

from config import UVICORN_HOST, UVICORN_PORT, image_tagging_config
from image_tagging_api import ImageTaggingAPI

app = FastAPI()
Instrumentator().instrument(app).expose(app)

image_tagging_api = ImageTaggingAPI(image_tagging_config)

@app.post("/tag_image_url")
async def tag_image_url(
    image_url: str = Form(...)
):
    response = image_tagging_api.get_image_tags_with_confidence(image_url=image_url, mode='file')
    return response

def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host=UVICORN_HOST, port=int(UVICORN_PORT))


if __name__ == '__main__':
    run()
