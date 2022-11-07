import uvicorn
from fastapi import FastAPI, File, Form, UploadFile
from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn.config import LOGGING_CONFIG

from config import UVICORN_HOST, UVICORN_PORT, email_delivery_config
from email_delivery_api import EmailDeliveryAPI

app = FastAPI()
Instrumentator().instrument(app).expose(app)

email_delivery_api = EmailDeliveryAPI(email_delivery_config)

@app.post("/send_email")
async def send_email(
    email: str = Form(...),
    subject: str = Form(...),
    text: str = Form(...)
):
    response = email_delivery_api.send_email(email, subject, text)
    return response

def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host=UVICORN_HOST, port=UVICORN_PORT)


if __name__ == '__main__':
    run()
