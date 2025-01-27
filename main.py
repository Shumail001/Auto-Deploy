import json
import os
import uuid
from dotenv import load_dotenv
import boto3
from fastapi import HTTPException
load_dotenv()

sqs_client = boto3.client("sqs",
                          region_name=os.getenv("AWS_DEFAULT_REGION"),
                          aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
                          )  # Replace with your region
sqs_queue_url = "https://sqs.us-east-1.amazonaws.com/054037101129/Video-Editor-Queue.fifo"

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



creative_id = "02b1c130-ef66-4b24-a9f0-da1156e5d82a1"
data = {
        "projectSettings": {
            "resolution": "1920x1080",
            "frameRate": "30fps",
            "filename": "temp",
            "aspectRatio": "16:9",
            "codec": "H.264",
            "exportSettings": {
                "bitrate": "4000k",
                "fileFormat": "mp4"
            }
        },
        "tracks": {
            "videoTracks": [
                {
                    "trackId": "video1",
                    "clips": [
                        {
                            "clipId": "clip1",
                            "source": "s3://fibonacci-json-2-video/test-videos/test1.mp4",
                            "storageType": "S3",
                            "startInSource": "00:00:00",
                            "duration": "03s",
                            "startInTimeline": "00:00:10",
                            "transformations": {
                                "scale": {"width": 1280, "height": 720},
                                "position": {"x": 0, "y": 50}
                            },
                            "audio": {
                                "volume": 0.9,
                                "fadeIn": "2s",
                                "fadeOut": "2s"
                            },
                            "transitions": {
                                "in": {"type": "fade", "duration": "1s"},
                                "out": {"type": "crossfade", "duration": "1s"}
                            }
                        }
                    ]
                },
                {
                    "trackId": "video2",
                    "clips": [
                        {
                            "clipId": "clip2",
                            "source": "s3://fibonacci-json-2-video/test-videos/test2.mp4",
                            "storageType": "S3",
                            "startInSource": "00:00:00",
                            "duration": "07s",
                            "startInTimeline": "00:00:00",
                            "transformations": {
                                "scale": {"width": 1280, "height": 720},
                                "position": {"x": 0, "y": 0}
                            },
                            "audio": {
                                "volume": 0.9,
                                "fadeIn": "2s",
                                "fadeOut": "2s"
                            },
                            "transitions": {
                                "in": {"type": "fade", "duration": "1s"},
                                "out": {"type": "crossfade", "duration": "1s"}
                            }
                        }
                    ]
                }
            ],
            "audioTracks": [
                {
                    "trackId": "audio1",
                    "source": "s3://fibonacci-json-2-video/test-videos/relaxing-audio-for-yoga-131673.mp3",
                    "storageType": "S3",
                    "startInTimeline": "00:00:00",
                    "duration": "09s",
                    "effects": {
                        "noiseReduction": "medium",
                        "reverb": {"enabled": True, "roomSize": "medium"}
                    }
                }
            ]
        },
        "text": {
            "overlays": [
                {
                    "text": "Yasir Maqbool",
                    "font": "Arial",
                    "size": 24,
                    "color": "#FFFFFF",
                    "position": {"x": "center", "y": "bottom"},
                    "timing": {"start": "00:00:02", "end": "00:00:05"}
                }
            ]
        },
        "animations": {
            "motion": [
                {
                    "clipId": "clip1",
                    "zoom": {"from": 1.0, "to": 1.2, "duration": "5s"}
                }
            ]
        },
        "croppingAndResizing": {
            "crop": {"top": 0, "bottom": 0, "left": 0, "right": 0}
        }
    }
s3_bucket = "Test"
file_basename = "assets/video_12345abc"
review_id = 0

response = send_to_sqs(creative_id, data, s3_bucket, file_basename, review_id)
print(response)