from urllib import response
import uvicorn
from fastapi import FastAPI, File, Form, UploadFile
from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn.config import LOGGING_CONFIG

from config import UVICORN_HOST, UVICORN_PORT, psql_config, s3_config, rabbitmq_config, image_tagging_config
from process_ads_service import ProcessAdsService

app = FastAPI()
Instrumentator().instrument(app).expose(app)

post_ads_service = ProcessAdsService(psql_config, s3_config, rabbitmq_config, image_tagging_config)


@app.post("/process_ads")
async def post_new_ad(
    image_id : str = Form(...)
):
    response = post_ads_service.process_ads(image_id)
    # TODO: send email to user
    return response


def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host=UVICORN_HOST, port=UVICORN_PORT)


if __name__ == '__main__':
    run()
