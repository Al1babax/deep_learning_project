from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Cookie, Form, UploadFile, File, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import datetime as dt
from functions.parse_logs import whole_data, past_hour_data

app = FastAPI()

# Setup CORS
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World",
            "message": "This is the root of the API. Please use the /docs endpoint to see the API documentation."}


@app.get("/api/v1/data")
def get_data(response: Response):
    try:
        response.status_code = status.HTTP_200_OK
        return whole_data()
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}


@app.get("/api/v1/past_hour")
def get_past_hour(response: Response):
    try:
        response.status_code = status.HTTP_200_OK
        return past_hour_data()
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}
