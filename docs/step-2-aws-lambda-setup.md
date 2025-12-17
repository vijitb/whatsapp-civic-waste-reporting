Objective: Replace local Flask + ngrok setup with a serverless, production-ready backend using AWS Lambda and API Gateway.

Architecture Overview: WhatsApp → Twilio → API Gateway → AWS Lambda → Response

Step 2.1: Create AWS Lambda Function
1. Runtime: Python 3.11
2. Function name: wastebridge-whatsapp-webhook
3. Permissions: Basic Lambda execution role

Step 2.2: Handle Twilio Payload
1. Twilio sends data as application/x-www-form-urlencoded.
2. Lambda must:
   Decode body (handle base64 if required)
   Parse key-value pairs
   Log payload to CloudWatch

Step 2.3: Generate TwiML Response
1. Twilio expects a valid XML response.
2. The Lambda function returns: HTTP 200
3. Content-Type: application/xml
4. TwiML message body

Step 2.4: Create API Gateway
1. Type: HTTP API
2. Route: POST /whatsapp
3. Integration: Lambda function
4. Deployment stage: $default

Step 2.5: Configure Twilio Webhook

Update Twilio Sandbox settings (as done in sandbox step1): https://<api-gateway-url>/whatsapp
IMPORTANT: to add /whatsapp in the URL
Disable ngrok usage.

Step 2.6: Debugging & Observability
1. Use CloudWatch Logs for payload inspection
2. Log full event for troubleshooting

Common issues addressed:
1. Base64 encoding
2. Incorrect headers
3. Lambda exceptions

Outcome
1. Fully serverless WhatsApp webhook
2. Always-on, scalable backend
3. Production-grade setup suitable for civic pilots

Next Step

Proceed to persistent storage using DynamoDB and S3.
