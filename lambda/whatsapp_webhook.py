import json
import base64
from urllib.parse import parse_qs
from twilio.twiml.messaging_response import MessagingResponse

def lambda_handler(event, context):

    print("RAW EVENT:", json.dumps(event))

    body = event.get("body", "")

    # Handle base64 encoding (API Gateway)
    if event.get("isBase64Encoded", False):
        body = base64.b64decode(body).decode("utf-8")

    data = parse_qs(body)

    print("Incoming WhatsApp data:", data)

    resp = MessagingResponse()
    resp.message("Thank you for reporting the incident.")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/xml"
        },
        "body": str(resp)
    }
