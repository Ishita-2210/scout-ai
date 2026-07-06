# Scout
### AI-Powered Multi-Agent Disaster Education Assistant

Scout is an intelligent multi-agent assistant designed to help students affected by disasters continue their education without interruption.

It combines specialized AI agents with web search and long-term memory to provide personalized guidance for school admissions, scholarships, temporary housing, legal rights, counselling, and document recovery.

---

## Problem Statement

Natural disasters often interrupt education by displacing students, destroying important documents, and limiting access to schools and support services.

Students frequently struggle to find:

- Nearby schools
- Admission procedures
- Scholarships
- Temporary housing
- Lost document recovery
- Legal rights
- Emotional counselling

Information is fragmented across multiple government portals and organizations.

Scout unifies these services into a single AI assistant capable of understanding complex, multi-domain queries.

---

# Features

- Multi-Agent AI Architecture
- Intelligent Query Routing
- School Recommendation Assistance
- Scholarship Discovery
- Temporary Housing Guidance
- Lost Document Recovery
- Educational Legal Assistance
- Mental Health & Counselling Support
- Web Search Integration
- Long-Term User Memory
- Conversation History
- Modern Chat Interface

---

# Architecture

```
                    User
                      │
                      ▼
               Root Orchestrator
                      │
 ┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
 │          │          │          │          │          │
 ▼          ▼          ▼          ▼          ▼          ▼
School   Scholarship Housing  Documents  Legal  Counselling
 Agent      Agent      Agent      Agent     Agent     Agent
                      │
                      ▼
                 Search Tool
                      │
                      ▼
                 Serper Search API
```

---

# Tech Stack

## Backend

- Python
- FastAPI
- Google ADK
- Gemini
- SQLite
- Pydantic
- SQLAlchemy
- Serper API

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Axios
- React Markdown
- Lucide Icons

---

# Multi-Agent System

Scout consists of specialized agents responsible for individual domains.

| Agent | Responsibility |
|--------|----------------|
| Root Agent | Intent understanding and orchestration |
| School Agent | School recommendations and admissions |
| Scholarship Agent | Scholarships and financial aid |
| Housing Agent | Temporary housing and shelters |
| Document Agent | Lost certificates and document recovery |
| Legal Agent | Educational rights and legal guidance |
| Counselling Agent | Emotional support and counselling |

The Root Agent automatically determines which specialist agents are required and combines their responses into a unified answer.

---

# Long-Term Memory

Scout stores user preferences across conversations, including:

- Name
- Grade
- Location
- Education Board
- Preferred Language

This enables personalized responses while reducing repetitive questions.

---

# Search Integration

Scout performs real-time web searches using the Serper Search API to retrieve:

- Government portals
- School websites
- Scholarship information
- Official educational resources

---

# User Interface

The frontend provides:

- Responsive Chat Interface
- Markdown Rendering
- Clickable Links
- Copy Response Button
- Auto-Scrolling Conversation
- Suggestion Cards
- Typing Indicator
- Modern Sidebar Navigation

---

# Running the Project

## Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn backend.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Environment Variables

Create a `.env` file.

```
GEMINI_API_KEY=YOUR_API_KEY

SERPER_API_KEY=YOUR_API_KEY
```

---

# Example Queries

### Single Agent

- Find government schools near Bengaluru
- I lost my transfer certificate
- Show scholarships for Class 12 students

### Multi-Agent

- I lost my home in floods and need nearby schools and scholarships.

- My transfer certificate was destroyed and I need legal guidance for admission.

- I'm anxious after the disaster and need counselling along with school recommendations.

---

# Future Improvements

- Streaming AI Responses
- Rich School Cards
- Voice Interaction
- Multilingual Support
- Offline Disaster Knowledge Base
- Government API Integrations
- Authentication
- Deployment

---

# Project Structure

```
backend/
    agents/
    api/
    execution/
    memory/
    repositories/
    services/
    tools/

frontend/
    src/
        components/
        pages/
        services/
        types/
```

---

# Contributors

Developed as part of a disaster education assistance project.

---
