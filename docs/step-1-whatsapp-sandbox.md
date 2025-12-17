Objective: Establish a working WhatsApp → Backend connection using the Twilio WhatsApp Sandbox. This step validates inbound message handling before moving to a production-grade setup.

Prerequisites:
1. Twilio account
2. WhatsApp-enabled phone
3. Basic familiarity with HTTP webhooks
4. Python 3.x installed

Step 1.1: Enable WhatsApp Sandbox in Twilio
1. Log in to Twilio Console
2. Navigate to Messaging → Try it out → WhatsApp Sandbox
3. Note the sandbox WhatsApp number and join code

Step 1.2: Join Sandbox from Phone
1. From your phone, send the join message:
2. join <sandbox-code>
You should receive a confirmation from Twilio.

Step 1.3: Create Local Webhook (Flask)
1. A simple Flask app is used to receive incoming WhatsApp messages.

Key responsibilities:
1. Accept POST requests
2. Log incoming payload
3. Respond with valid TwiML

Step 1.4: Expose Local Server Using ngrok
1. Twilio requires a public HTTPS endpoint.
2. ngrok http 5000
3. Copy the generated HTTPS URL.

Step 1.5: Configure Twilio Webhook
Set following Twilio Sandbox settings:
 - When a message comes in: https://<ngrok-url>/whatsapp
 - Method: POST
Save configuration.

Step 1.6: Test End-to-End
1. Send any message from WhatsApp.
2. Success criteria:
    Flask server receives request
    Payload is logged

WhatsApp receives acknowledgment message

Outcome: WhatsApp → Backend communication validated

Payload format understood

Ready to migrate backend to AWS
