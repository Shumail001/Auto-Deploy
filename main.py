import json
import os
import uuid
from dotenv import load_dotenv
import boto3
from fastapi import FastAPI, HTTPException

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize SQS client
sqs_client = boto3.client("sqs",
                          region_name=os.getenv("AWS_DEFAULT_REGION"),
                          aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
                          )
sqs_queue_url = os.getenv("SQS_QUEUE_URL")

# Function to send message to SQS
def send_to_sqs(creative_id: str, data: dict, s3_bucket: str, file_basename: str, review_id: int):
    try:
        message_id = str(uuid.uuid4())
        sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=json.dumps({
                "creative_id": creative_id,
                "ad_json": data,
                "s3_bucket": s3_bucket,
                "file_basename": file_basename,
                "id": creative_id,
                "review_id": review_id,
            }),
            MessageGroupId="video-processing",
            MessageDeduplicationId=message_id
        )
        return {
            "creative_id": creative_id,
            "id": creative_id,
            "status": "task_queued",
            "message_id": message_id
        }
    except Exception as sqs_error:
        raise HTTPException(status_code=500, detail=f"Error sending message to SQS: {str(sqs_error)}")

# Home route
@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI SQS Service!"}

# API endpoint to send data to SQS
@app.post("/send")
def send_message(creative_id: str, data: dict, s3_bucket: str, file_basename: str, review_id: int):
    response = send_to_sqs(creative_id, data, s3_bucket, file_basename, review_id)
    return response
