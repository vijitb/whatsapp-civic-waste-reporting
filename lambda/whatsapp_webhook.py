import json
import base64
import uuid
import hashlib
import boto3
import requests
import os
from datetime import datetime
from urllib.parse import parse_qs
from twilio.twiml.messaging_response import MessagingResponse

# initialize dynamodb client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('waste_reports')

# initialize s3 client
s3 = boto3.client("s3")
BUCKET_NAME = "waste-report-images"

# initialize environment variables
# Store your twillio token and account id in environment variables
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")


def lambda_handler(event, context):

    print("RAW EVENT:", json.dumps(event))

    body = event.get("body", "")

    # Handle base64 encoding (API Gateway)
    if event.get("isBase64Encoded", False):
        body = base64.b64decode(body).decode("utf-8")

    data = parse_qs(body)

    # get phone number and message from user's response
    phone = data.get("From", [""])[0]
    message = data.get("Body", [""])[0]

    report_id = str(uuid.uuid4())
    reporter_hash = hashlib.sha256(phone.encode()).hexdigest()

    print("Incoming WhatsApp data:", data)

    # image capturing logic
        # Twilio Media Payload
        # 1. NumMedia (no. of images)
        # 2. MediaUrl0, MediaUrl1, MediaUrl2, ... (image url)
        # 3. MediaContentType0, MediaContentType1, MediaContentType2, ... (image/jpeg)
    try:
        num_media = int(data.get("NumMedia", [0])[0])
        images_urls = []

        if num_media > 0:
            for i in range(num_media):
                media_url = data.get(f"MediaUrl{i}", [""])[0]
                media_content_type = data.get(f"MediaContentType{i}", [""])[0]

                if media_content_type.startswith("image"):
                    image_bytes = download_twilio_media(media_url)
                    s3_path = upload_to_s3(image_bytes, report_id)
                    images_urls.append(s3_path)
    except Exception as e:
        print("Error processing image:", str(e))

    resp = MessagingResponse()
    resp.message("Thank you for reporting the incident.")

    item = {
        "report_id": report_id,
        "created_at": datetime.utcnow().isoformat(),
        "issue_type": "unspecified",
        "description": message,
        "status": "open",
        "source": "whatsapp",
        "reporter_hash": reporter_hash,
        "images_urls": images_urls
    }

    table.put_item(Item=item)

    resp = MessagingResponse()
    resp.message(f"Thank you. Your report ID is {report_id[:8]}")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/xml"
        },
        "body": str(resp)
    }


def download_twilio_media(media_url):
    response = requests.get(
        media_url,
        auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    )

    response.raise_for_status() # prevents silent failures
    return response.content


def upload_to_s3(image_bytes, report_id):
    key = f"reports/{report_id}.jpg"
    
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=image_bytes,
        ContentType="image/jpeg"
    )
    
    return f"s3://{BUCKET_NAME}/{key}"
