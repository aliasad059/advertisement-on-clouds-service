import uvicorn
from fastapi import FastAPI, Form
from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn.config import LOGGING_CONFIG
import requests
from config import UVICORN_HOST, UVICORN_PORT, psql_config, s3_config, EMAIL_DELIVERY_SERVICE_URL, EMAIL_PROCESSED_SUBJECT, EMAIL_PROCESSED_TEXT
from process_ads_service import ProcessAdsService

app = FastAPI()
Instrumentator().instrument(app).expose(app)

post_ads_service = ProcessAdsService(psql_config, s3_config)


@app.post("/process_ads")
async def process_ads(
    image_id : str = Form(...)
):
    response = post_ads_service.process_ads(image_id)
    if response['status'] == 'failed':
        return response
    elif response['status'] == 'approved':
        RESULT =f' REQUEST_ID: {response["request_id"]},\n STATUS: {response["status"]},\n CATEGORY: {response["category"]},\n DESCRIPTION: {response["description"]},\n EMAIL: {response["email"]}'
    elif response['status'] == 'rejected':
        RESULT =f' REQUEST_ID: {response["request_id"]},\n STATUS: {response["status"]},\n DESCRIPTION: {response["description"]},\n EMAIL: {response["email"]}'

    send_email(response['email'], EMAIL_PROCESSED_SUBJECT, EMAIL_PROCESSED_TEXT.replace("REQUEST_ID", image_id).replace("RESULT", RESULT))    
    return response

def send_email(email, subject, text):
    requests.post(
        EMAIL_DELIVERY_SERVICE_URL,
        data={
            "email": email,
            "subject": subject,
            "text": text
            }
    )

def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host=UVICORN_HOST, port=int(UVICORN_PORT))


if __name__ == '__main__':
    run()
