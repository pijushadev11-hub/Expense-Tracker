# Expense Tracker - FastAPI + React

A scalable expense tracking application with FastAPI backend and React frontend.

## Architecture

### Backend (FastAPI + SQLAlchemy + PostgreSQL)
- **Authentication**: OAuth integration (Google, Apple) with JWT tokens
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API**: RESTful endpoints with automatic OpenAPI documentation
- **Features**: Monthly aggregation, category breakdown, budget insights

### Frontend (React + Tailwind CSS)
- **Authentication**: OAuth login with Google/Apple
- **Dashboard**: Interactive charts and monthly summaries
- **Forms**: Transaction entry with real-time validation
- **Responsive**: Mobile-first design

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### Setup

1. **Backend setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   
   # Set up database
   psql -U postgres -f schema.sql
   
   # Update .env with your OAuth credentials and database URL
   
   # Start server
   python run.py
   ```

2. **Frontend setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

## API Documentation

FastAPI automatically generates interactive API docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## OAuth Setup

### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add `http://localhost:8000/api/auth/google/callback` to redirect URIs
6. Update `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`

### Apple OAuth
1. Go to [Apple Developer](https://developer.apple.com/)
2. Create App ID and Services ID
3. Configure Sign in with Apple
4. Add `http://localhost:8000/api/auth/apple/callback` to redirect URIs
5. Update `APPLE_CLIENT_ID` and `APPLE_CLIENT_SECRET` in `.env`

## Database Schema

- **users**: OAuth user profiles
- **transactions**: Income/expense entries
- **monthly_summaries**: Computed aggregations for performance

## Features

✅ **Implemented**
- OAuth authentication (Google, Apple)
- Transaction CRUD with automatic monthly summaries
- Dashboard with charts and category breakdown
- Responsive React frontend

🚧 **Roadmap**
- Budget alerts and notifications
- Advanced analytics and insights
- Export functionality (PDF, CSV)
- Mobile app (React Native)
- Real-time updates with WebSockets