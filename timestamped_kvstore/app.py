from contextlib import asynccontextmanager
from fastapi import FastAPI
from timestamped_kvstore.models import KeyTimestamp, UpdateValue


@asynccontextmanager
async def lifespan(app: FastAPI):
    # set up something
    yield
    # destroy something


app = FastAPI(lifespan=lifespan)


TRINO_CONN_STR = (
    "DRIVER=Simba Trino ODBC Driver;"
    "HOST=localhost;"
    "PORT=8080;"
    "Catalog=iceberg;"
    "Schema=default;"
    "UID=trino;"
    "PWD=;"
)


@app.put("/")
def put_data(req_body: UpdateValue):
    return req_body


@app.get("/")
def get_data(req_body: KeyTimestamp):
    return req_body
