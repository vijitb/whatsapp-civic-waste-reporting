STEP 3: Data Storage Design & Implementation (DynamoDB + S3 | AWS Free Tier | Civic-ready)

Goal of STEP 3

After this step, we will be able to:
1. Store photos of waste incidents
2. Persist citizen complaints
3. Capture geo-location
4. Track complaint lifecycle
5. Enable NGO / municipal analytics

STEP 3.1: Data Design (Design Principles)
1. Minimal PII
2. Citizen-first privacy
3. Municipality-ready
4. Queryable by location & status

STEP 3.2: Create DynamoDB Table 

_Table Name: waste_reports_

Attribute	
Type.........................report_id (PK)	String (UUID)
report_id....................Unique complaint ID
created_at...................ISO timestamp
issue_type...................dumping / missed pickup / no bin
description..................User message
latitude.....................Decimal
longitude....................Decimal
image_urls...................List (S3 paths)
status.......................open / in_progress / resolved
source.......................whatsapp
reporter_hash................SHA-256 of phone

_Phone numbers are never stored in plain text_

STEP 3.3: Create S3 Bucket (for storing images)

_Bucket Name: waste-report-images-<your-unique-id>_
Block public access: ON

Folder structure (logical):
s3://bucket-name/
└── reports/
    └── 2025/
        └── 09/
            └── report_id.jpg


STEP 3.4: Update Lambda to Store Data

Attach these permissions to Lambda role:
1. AmazonDynamoDBFullAccess (for pilot)
2. AmazonS3PutObject
