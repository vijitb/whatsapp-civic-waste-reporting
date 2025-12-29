import json
import base64
import uuid
import hashlib
import boto3
from datetime import datetime
from urllib.parse import parse_qs
from twilio.twiml.messaging_response import MessagingResponse

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('waste_reports')

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

    resp = MessagingResponse()
    resp.message("Thank you for reporting the incident.")

    item = {
        "report_id": report_id,
        "created_at": datetime.utcnow().isoformat(),
        "issue_type": "unspecified",
        "description": message,
        "status": "open",
        "source": "whatsapp",
        "reporter_hash": reporter_hash
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
