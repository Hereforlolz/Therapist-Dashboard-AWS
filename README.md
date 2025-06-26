# Therapist Dashboard

My therapist mentioned she spends way too much time on paperwork instead of actually helping people. So I built this to fix that problem.

## What it does

- Stores patient session summaries in DynamoDB
- Uses Claude AI (through AWS Bedrock) to generate insights from messy session notes
- Simple REST API that actually works
- Built with HIPAA requirements in mind (though not fully compliant yet)

## Tech Stack

**Backend:** AWS Lambda + API Gateway (Node.js)  
**Database:** DynamoDB  
**AI:** Claude via AWS Bedrock  
**Frontend:** React (deployed on Render)

## API Endpoints

```
GET /dashboard     - List patient summaries
POST /insight      - Generate insights from session notes  
POST /summary      - Save/update patient summary
```

## Architecture

React app → API Gateway → Lambda functions → Bedrock/DynamoDB

I have three main Lambda functions handling the core functionality:
- Patient data retrieval
- Session note storage
- AI insight generation via Claude

## Setup

1. Clone this repo
2. Create a DynamoDB table called `patients` 
3. Configure AWS Bedrock access for Claude
4. Deploy the Lambda functions (AWS Console or SAM CLI)
5. Test the endpoints with curl or Postman

## Current Status

This is a working MVP that demonstrates the core concept. Still working on proper authentication and full HIPAA compliance, but the foundation is solid.

## What's Next

- User authentication and role-based access
- Multi-session pattern analysis
- Better risk detection capabilities
- Full HIPAA compliance
- Potential EHR integration

The goal is to help therapists focus on what they do best - helping people - instead of drowning in paperwork.