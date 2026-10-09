# Setup Guide - Mewtwo (Autonomous Disaster Response Planner)

## Prerequisites
Before you begin, ensure you have the following installed:
- [ ] Python 3.11+
- [ ] Node.js 18+
- [ ] MongoDB (Local or Atlas)
- [ ] IBM Bob access

## Environment Variables
Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
| Variable | Description | Required |
|------------------|---------------------|------------|
| `IBM_BOB_API_KEY` | Your IBM Bob API key | Yes |
| `DATABASE_URL` | MongoDB connection string | Yes |

INSTALLATION
# 1. Clone the repository
git clone https://github.com/shlokparmar740/bob-ai-hackathon--TEAM-FLUXO-.git
cd bob-ai-hackathon--TEAM-FLUXO-

# 2. Install backend dependencies
pip install -r requirements.txt

# 3. Install frontend dependencies (if applicable)
cd frontend && npm install

RUNNING
# Start the backend
uvicorn src.main:app --reload

# Start the frontend
cd frontend && npm run dev

The application will be available at: http://localhost:3000  #(if applicable)

RUNNING-TESTS

pytest tests/ -v



