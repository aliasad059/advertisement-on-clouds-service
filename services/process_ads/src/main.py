import uvicorn
from fastapi import FastAPI, Form
from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn.config import LOGGING_CONFIG

from config import UVICORN_HOST, UVICORN_PORT, psql_config, s3_config
from process_ads_service import ProcessAdsService

app = FastAPI()
Instrumentator().instrument(app).expose(app)

post_ads_service = ProcessAdsService(psql_config, s3_config)


@app.post("/process_ads")
async def process_ads(
    image_id : str = Form(...)
):
    response = post_ads_service.process_ads(image_id)
    # TODO: send email to user
    return response


def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host=UVICORN_HOST, port=int(UVICORN_PORT))


if __name__ == '__main__':
    run()
