import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn.config import LOGGING_CONFIG

from post_advs_service import PostAdvsService

load_dotenv()
app = FastAPI()
Instrumentator().instrument(app).expose(app)

post_advs_service = PostAdvsService()


@app.post("/post_advs")
async def post_advs(
    image : UploadFile = File(...),
    description : str = Form(...),
    email : str = Form(...)
):
    request_id = post_advs_service.post_advs(image, description, email)
    # TODO: send email to user
    return {"request_id": request_id}


@app.post("/get_request_status")
async def get_request_status(
    request_id : str = Form(...)
):  
    request_status = post_advs_service.get_request_status(request_id)
    return {"request_status": request_status}

def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host=os.getenv('UVICORN_HOST'), port=os.getenv('UVICORN_PORT'))


if __name__ == '__main__':
    run()
