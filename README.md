# 🧠 AI-Powered Therapist Dashboard

> Serverless AI to cut therpaist burnout and boost session impact
🧠 This project was entirely self-initiated and built solo. I used AI tools like Claude, Gemini, and ChatGPT to assist with parts of the architecture, coding, and documentation - but the core idea, execution, and implementation are 100% mine.

## 🎯 Problem Statement

**My therapist told me Therapists spend 40% of their time on paperwork instead of helping patients.**

Traditional therapy practices involve:
- ✋ 30-45 minutes per session notes per session for insurance SOAP NOTES
- 📝 Subjective treatment planning
- 🔄 Repetitive admin work
- 📊 not a lot of visibilty on long-term patient progress or holistic view

As someone obsessed with automation that actually helps people, I knew this had to change.

**My solution:** AI-powered serverless dashboard that automates documentation and generates actionable insights in seconds that can beHIPAA compliant and used for insurance notes.

---

## 🚀 Solution Overview

### What it Does
This is a fully serverless AI dashboard that lets therapists:

    ✅ Auto-generate structured session summaries

    ✅ Get treatment insights from Claude (via AWS Bedrock)

    ✅ See patient progress in one clean place

    ✅ Forget infrastructure headaches- it just works

### Big Wins

- ⏰ **Saves 2-3 hours daily** per therapist
- 🧠 **AI-enhanced insights** improve treatment quality  
- 💰 **Cost-effective** pay-per-use model
- 🔒 **HIPAA-ready** AWS infrastructure
- 📈 **Infinitely scalable** no DevOps stress

---

## 🛠️ How I built it

### AWS architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Client  │◄──►│   API Gateway    │◄──►│ Lambda Functions│
│                 │    │  (REST Endpoints)│    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                ▲                        │
                                │                        ▼
                       ┌────────────────┐      ┌─────────────────┐
                       │   CloudWatch   │      │   AWS Bedrock   │
                       │   (Monitoring) │      │  (Claude AI)    │
                       └────────────────┘      └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   DynamoDB      │
                                               │ (Patient Data)  │
                                               └─────────────────┘
```

### 🔧 Key Lambda Functions

    GET /dashboard-  Fetches patient summaries

    POST /summary-  Saves or updates summaries

    POST /insight-  Sends notes to Claude AI & returns personalized insights

Everything’s CORS-ready, error-handled, and stateless.

### 🔐 Security & HIPAA-Readiness

Built with HIPAA in mind:

    🔒 Data encrypted at rest & in transit

    🔑 IAM roles + API key auth

    📜 CloudWatch logging for traceability

    🌐 HTTPS only, input validation, and no sensitive data leaks in errors

    AWS handles most of the heavy lifting , but I double-checked against HIPAA best practices just to be sure.

## 📋 API Endpoints

| Method | Endpoint | Lambda Function | Description |
|--------|----------|-----------------|-------------|
| `GET` | `/dashboard` | dashboard-function | Retrieve all patient summaries |
| `POST` | `/insight` | insight-generator | Generate AI session insights |
| `POST` | `/summary` | summary-manager | Save/update patient data |

### Example API Usage

```bash
# Get patient dashboard
curl https://pkw8rjj2r8.execute-api.us-east-1.amazonaws.com/Prod/dashboard

# Generate session insight
curl -X POST https://pkw8rjj2r8.execute-api.us-east-1.amazonaws.com/Prod/insight \
  -H "Content-Type: application/json" \
  -d '{"sessionNotes": "Patient discussed anxiety management..."}'
```

---

# 🚀 Deployment Guide
## Backend

Set up DynamoDB
    aws dynamodb create-table --table-name patients ...
 Deploy Lambda
    zip dashboard-function.zip dashboard/
    aws lambda create-function ...

## Frontend (Render.com)

    REACT_APP_API_BASE_URL=https://your-api-gateway-url/Prod

    npm install && npm run build

    Live demo deployed via Render


## 🎥 Demo Features

### Live Functionality
📽️ What You Can Do in the Demo

    🧑‍⚕️ View patients & summaries - Refresh the page if no patient data found

    ✍️ Paste session notes → get AI insights

    📊 See recommendations powered by Claude

    🚀 No servers, just smooth scaling
---
### 🔮 Roadmap (Next 3 Months)

    Multi-session pattern tracking

    Outcome scoring

    Early risk flags (e.g. depressive patterns)

    Smarter treatment flows

## 🤝 Want to Contribute?

This was build for the AWS Lambda hackathon as a prototype to help my therpaist pay more attention to me without getting burnout documenting.
This was built fast and solo - so if you want to help out (or suggest features from a therapist’s perspective), I’m all ears.

--- 
git clone https://github.com/Hereforlolz/Therapist-Dashboard-AWS
cd ui && npm install && npm start
---

## 📞 Contact & Support

**Created by**: Sreenidhi  
**GitHub**: [Hereforlolz](https://github.com/Hereforlolz)  
**Demo**: [Live Application](https://your-render-app.onrender.com)  
**Video**: [3-Minute Demo](https://youtube.com/watch?v=your-video-id)

---

## 📄 License

This project is licensed under the MIT License

---

*Built with ❤️ for therapists worldwide, powered by AWS Lambda serverless magic*