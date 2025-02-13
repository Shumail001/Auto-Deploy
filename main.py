import json
import os
import uuid
from dotenv import load_dotenv
import boto3
from fastapi import FastAPI, HTTPException
app = FastAPI(title="Leonardo Video Edits")
# Home route
@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI SQS Service!"}
