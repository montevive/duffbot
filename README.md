# Duffbot: AI Tool Preference Collector

## Overview

Duffbot is an AI agent that collects user preferences about AI tools used in daily operations and displays a real-time scoreboard of the most popular tools. The project aims to help users discover and optimize their AI tool usage based on crowd-sourced preferences. It uses FastAPI for the backend, Gradio for the frontend, LlamaIndex for advanced AI agent capabilities, and PostgreSQL with pgVector for efficient data storage and vector operations.

## Features

- User-friendly Gradio interface for submitting AI tool preferences
- Real-time updating scoreboard of top AI tools
- Categorization of tools by use case (e.g., productivity, coding, design)
- Anonymous data collection to protect user privacy
- FastAPI backend for efficient data processing and storage
- LlamaIndex integration for advanced AI agent capabilities

## Tech Stack

- Backend: FastAPI
- Frontend: Gradio
- AI Agent: LlamaIndex
- Database: Redis

## Prerequisites

- Python 3.7+
- pip
- PostgreSQL 11+
- pgVector extension for PostgreSQL

## Project Structure

### Components

1. Backend (FastAPI)
   - Main API (`main.py`)
   - Routers:
     - Chat (`chat.py`)
     - Scoreboard (`scoreboard.py`)
   - Services:
     - Agent (`agent.py`)
     - Tool (`tool.py`)
   - Schemas (`schemas.py`)

2. Frontend
   - Scoreboard (React + TypeScript + Vite)
   - Chatbot Interface (Gradio)

### Directory Explanation

- `backend/`: Contains the FastAPI application and related files
  - `main.py`: Main FastAPI application entry point
  - `schemas.py`: Pydantic schemas for request/response models
  - `routers/`: API route handlers
- `frontend/`: Contains the Gradio interface
  - `gradio_app.py`: Gradio application for user interaction
- `tests/`: Unit and integration tests
- `config/`: Configuration files and environment variables
- `requirements.txt`: Project dependencies
- `README.md`: Project documentation (this file)
- `.gitignore`: Specifies intentionally untracked files to ignore

## Installation

```bash
git clone https://github.com/montevive/duffbot.git
cd duffbot
pip install -r requirements.txt

## Usage

1. Start the FastAPI backend:

```
uvicorn backend.main:app --reload
```

2. In a new terminal, start the Gradio frontend:

```
python frontend/gradio_app.py
``

3. Open a web browser and navigate to the URL provided by Gradio (typically http://localhost:8001)
4. Submit your AI tool preferences using the Gradio interface
5. View the real-time scoreboard to see the most popular tools

# API Documentation

After starting the FastAPI server, you can view the API documentation at http://localhost:8000/docs.


# Contributing

We welcome contributions to improve Duffbot! Please follow these steps:

1. Fork the repository
2. Create a new branch: git checkout -b feature/your-feature-name
3. Make your changes and commit them: git commit -m 'Add some feature'
4. Push to the branch: git push origin feature/your-feature-name
5. Submit a pull request

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Contact
If you have any questions or suggestions, please open an issue or contact the maintainer at info@montevive.ai.

# Acknowledgements
- Thanks to all contributors who have helped shape Duffbot
- FastAPI for providing a modern, fast (high-performance) web framework for building APIs
- Gradio for simplifying the creation of web interfaces for ML models
- LlamaIndex for enhancing our AI agent capabilities
- Inspired by the need for better AI tool discovery and optimization