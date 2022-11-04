from urllib import response
import uvicorn
from fastapi import FastAPI, File, Form, UploadFile
from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn.config import LOGGING_CONFIG

from config import UVICORN_HOST, UVICORN_PORT, psql_config, s3_config, rabbitmq_config
from post_ads_service import PostAdsService

app = FastAPI()
Instrumentator().instrument(app).expose(app)

post_ads_service = PostAdsService(psql_config, s3_config, rabbitmq_config)


@app.post("/post_new_ad")
async def post_new_ad(
    image : UploadFile = File(...),
    description : str = Form(...),
    email : str = Form(...)
):
    response = post_ads_service.post_ads(image, description, email)
    # TODO: send email to user
    return response


@app.post("/get_request_status")
async def get_request_status(
    request_id : str = Form(...)
):  
    request_status = post_ads_service.get_request_status(request_id)
    return request_status

def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host=UVICORN_HOST, port=UVICORN_PORT)


if __name__ == '__main__':
    run()
