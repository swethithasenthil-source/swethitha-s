# 5. Project Development

## Development Environment

The project was developed using:

- Python
- Visual Studio Code
- FastAPI
- Streamlit/Web Frontend
- Google Gemini API
- Git
- GitHub

## Backend

The backend is developed using FastAPI.

Main responsibilities:

- Receive frontend requests
- Validate input
- Process documents
- Communicate with the AI service
- Return generated results
- Handle document exports

## Frontend

The frontend provides the user interface.

Main functions:

- Accept user input
- Upload documents
- Display AI-generated results
- Provide document-related actions
- Allow users to download results

## AI Integration

The project integrates an AI language model to analyze
and generate responses based on the provided legal information.

## Document Export

The project supports generating output documents in formats
such as:

- TXT
- PDF
- DOCX

## Development Structure

```text
5. Project Development/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   └── services/
│
├── frontend/
│   └── app.py
│
├── requirements.txt
└── development.md
