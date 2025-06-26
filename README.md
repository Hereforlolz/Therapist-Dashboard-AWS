# Therapist Dashboard

My therapist mentioned she spends way too much time on notes instead of actually helping people. So I built this to fix that problem.

## What it does
- Stores patient session summaries in DynamoDB
- Uses Claude AI (through AWS Bedrock) to generate insights from raw notes
- Simple REST API that actually works
- Built to handle HIPAA requirements (though not fully compliant yet)

## Tech stuff
**Backend:** AWS Lambda functions + API Gateway  
**Database:** DynamoDB  
**AI:** Claude via Bedrock  
**Frontend:** React app  

## API Endpoints
```
GET /dashboard - gets patient list
POST /summary - saves session notes
POST /insight - sends notes to AI, gets back suggestions
```

## Setup
1. Clone this repo
2. Set up a DynamoDB table called `patients`
3. Configure AWS Bedrock access
4. Deploy the Lambda functions
5. Test with curl or Postman

Still working on proper auth and full HIPAA compliance, but the core functionality is there.

