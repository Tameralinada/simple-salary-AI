# Finance Manager

A Flask-based financial management application with AI-powered transaction categorization and insights.

## Features

- Automatic transaction categorization using AI
- German tax calculation
- Financial insights using LLM
- Transaction history tracking
- SQLite database storage

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run.py
```

## API Endpoints

- POST `/classify_transaction`: Classify and save a new transaction
  - Required fields: description (string), amount (float)
  
- POST `/financial_insights`: Get AI-powered insights about your finances
  - Required fields: question (string)
  
- GET `/transactions`: Retrieve all transactions

## Dependencies

See `requirements.txt` for a full list of dependencies.
