## Therapist Dashboard AI — AWS Lambda Prototype

A minimal AI-augmented therapist dashboard leveraging AWS Lambda, DynamoDB, and Bedrock Claude to automate session note summaries and generate gentle, actionable insights.

Features:
✅ Secure patient summary storage (DynamoDB)
✅ Real-time AI insights powered by Bedrock Claude
✅ Serverless architecture with Lambda + API Gateway
✅ Designed for easy expansion to HIPAA compliance

Endpoints:

    GET /dashboard → List patient summaries

    POST /insight → Generate new session insight

    POST /summary → Save updated patient summary

Architecture:
💡 Bedrock: Claude 3 Sonnet
🗂️ DynamoDB: Patients table
☁️ Lambda: 3 serverless functions
🌐 API Gateway: Secure REST API

How to deploy:

    Clone this repo

    Create the DynamoDB table patients

    Configure Bedrock access and model ID

    Deploy Lambdas via AWS Console or SAM CLI

    Test endpoints with Postman or curl

Future ideas:

    Therapist login & role-based access control

    Full HIPAA-compliant storage & audit logging

    EHR integration for seamless clinical workflows

