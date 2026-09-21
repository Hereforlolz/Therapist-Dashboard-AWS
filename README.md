# Therapist Dashboard (AWS prototype)

A serverless prototype that stores therapist session summaries and uses Claude
(via AWS Bedrock) to draft insights from session notes. Follow-on to
[CompassionateConnect AI](https://github.com/Hereforlolz/Compassionate-connect).

> **Status: archived prototype. Not a clinical or production system.**
> Use synthetic data only. It has no authentication, is **not HIPAA-compliant**,
> has not been clinically validated, and has not been tested with real users or
> patients. AI output is a draft for a clinician to review, never a decision.
> The deployed backend and frontend have been shut down.

## What it does

- Stores patient summaries in DynamoDB
- Generates draft insights from session notes with Claude on Bedrock
- Exposes a small REST API consumed by a React frontend

## Tech stack

- **Backend:** AWS Lambda (Python 3.9) + API Gateway, defined in `template.yaml` (SAM)
- **Database:** DynamoDB (`patients` table, pay-per-request)
- **AI:** Claude 3 Sonnet via AWS Bedrock (`anthropic.claude-3-sonnet-20240229-v1:0`)
- **Frontend:** React (`therapist-dashboard-ui/`), reads the API URL from `REACT_APP_API_BASE_URL`

## API

```
GET  /dashboard   List patient summaries
POST /insight     Generate insights from session notes
POST /summary     Save or update a patient summary
```

Flow: React app → API Gateway → Lambda → DynamoDB / Bedrock.

## Known limitations

These are real gaps, listed so nobody mistakes this for a compliant system:

- **No authentication or authorization.** Endpoints are open, and CORS allows any origin (`*`).
- **Over-broad IAM.** Each function has `AmazonDynamoDBFullAccess` and `AmazonBedrockFullAccess`; it needs least-privilege policies.
- **Full-table `Scan`** returns patient names for the dashboard.
- **No compliance work done.** No BAA, audit logging, retention policy, or encryption/key configuration beyond AWS defaults. "HIPAA-aligned" would not be an accurate description.
- **Frontend test is the unmodified create-react-app sample** and would fail.
- **No automated tests** for the Lambdas, and no evaluation of AI output quality.

## Setup (to run your own copy)

1. Have an AWS account with Bedrock model access for Claude 3 Sonnet in your region.
2. `sam build && sam deploy --guided` (creates the table, API, and functions).
3. Set `REACT_APP_API_BASE_URL` to the deployed API URL and run the UI in `therapist-dashboard-ui/`.
4. Costs apply. Delete the stack when finished (`sam delete`).

## If this were taken further

- Authentication and role-based access first, before any other feature
- Least-privilege IAM, a proper compliance review, audit logging
- A clinician review step for all AI-generated content
- Evaluation of insight quality on synthetic cases
