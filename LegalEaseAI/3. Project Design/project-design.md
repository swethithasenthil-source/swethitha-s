# 3. Project Design

## System Overview

LegalEaseAI consists of a frontend, backend, AI service,
document processing services, and export services.

## Architecture

User
  |
  v
Frontend
  |
  v
FastAPI Backend
  |
  +----------------------+
  |                      |
  v                      v
Document Processing    Gemini AI
  |                      |
  +----------+-----------+
             |
             v
       Generated Result
             |
             v
          Frontend
             |
             v
       Export / Download

## Main Components

### Frontend

Provides the user interface for entering information,
uploading documents, and viewing results.

### Backend

Handles API requests and connects the frontend with the
AI and document-processing services.

### AI Module

Uses an AI/LLM service to analyze and generate responses
based on the provided legal content.

### Document Processing

Handles extraction and processing of document information.

### Export Module

Generates downloadable output such as TXT, PDF, or DOCX.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| Backend | FastAPI |
| AI | Google Gemini |
| Frontend | Streamlit / Web UI |
| Development Tool | VS Code |
| Version Control | GitHub |

## Data Flow

1. User enters or uploads information.
2. Frontend sends the request to the backend.
3. Backend validates the request.
4. Document content is processed.
5. AI service analyzes the content.
6. Generated response is returned.
7. Frontend displays the result.
8. User can export the result.
