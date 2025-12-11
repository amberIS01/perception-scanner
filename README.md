# Hello World - FastAPI + React + shadcn/ui

A full-stack application with a Python FastAPI backend and a React TypeScript frontend using shadcn/ui components.

## Project Structure

```
.
├── backend/          # FastAPI backend
│   ├── main.py
│   └── requirements.txt
└── frontend/         # React frontend with shadcn/ui
    ├── src/
    │   ├── components/
    │   │   └── ui/
    │   ├── lib/
    │   └── App.tsx
    └── package.json
```

## Backend Setup (FastAPI)

### Prerequisites
- Python 3.8+

### Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the Backend

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

API Endpoints:
- `GET /` - Returns a simple hello world message
- `GET /api/hello` - Returns a hello world message from FastAPI

## Frontend Setup (React + shadcn/ui)

### Prerequisites
- Node.js 18+
- npm

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

### Run the Frontend

```bash
npm run dev
```

The application will be available at http://localhost:5173

## Running Both Servers

You'll need two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

## Features

- FastAPI backend with CORS support
- React frontend with TypeScript
- shadcn/ui components (Button, Card)
- Tailwind CSS for styling
- Full-stack "Hello World" integration

## Technologies Used

### Backend
- FastAPI
- Uvicorn
- Python

### Frontend
- React 18
- TypeScript
- Vite
- shadcn/ui
- Tailwind CSS
- Radix UI

## Development

The frontend is configured to communicate with the backend at http://localhost:8000. The backend has CORS enabled for http://localhost:5173.
