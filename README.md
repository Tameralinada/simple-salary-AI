# Simple Salary AI - Finance Manager

A sophisticated Flask-based financial management application that leverages AI to help you manage your finances more effectively. The application provides automatic transaction categorization, German tax calculations, and AI-powered financial insights.

## 🌟 Features

- **AI-Powered Transaction Categorization**
  - Automatic categorization of transactions using machine learning
  - Smart pattern recognition for recurring transactions
  - Custom category management

- **German Tax Calculations**
  - Automatic tax class determination
  - Monthly tax estimates
  - Annual tax summaries
  - Support for various income types

- **Financial Insights with LLM**
  - Natural language queries about your finances
  - Spending pattern analysis
  - Budget recommendations
  - Future expense predictions

- **Transaction Management**
  - Detailed transaction history
  - Search and filtering capabilities
  - Export functionality
  - Bulk import support

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Tameralinada/simple-salary-AI.git
cd simple-salary-AI
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python run.py
```

5. Access the application at: http://localhost:5000

## 💻 Usage

### Web Interface

The application provides an intuitive web interface where you can:
- Add new transactions
- View transaction history
- Generate financial insights
- Calculate taxes
- Export reports

### API Endpoints

#### Transaction Management
- `POST /classify_transaction`
  - Classify and save a new transaction
  - Required fields: 
    - `description` (string)
    - `amount` (float)
  - Returns: Transaction details with category

#### Financial Insights
- `POST /financial_insights`
  - Get AI-powered insights about your finances
  - Required fields:
    - `question` (string)
  - Returns: Detailed financial analysis

#### Transaction History
- `GET /transactions`
  - Retrieve all transactions
  - Optional query parameters:
    - `start_date` (YYYY-MM-DD)
    - `end_date` (YYYY-MM-DD)
    - `category` (string)

## ⚙️ Configuration

The application can be configured through environment variables or a `.env` file:

```env
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///instance/finance.db
SECRET_KEY=your-secret-key
```

## 📦 Project Structure

```
simple-salary-AI/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   └── templates/
│       └── index.html
├── instance/
├── venv/
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- GitHub Repository: [https://github.com/Tameralinada/simple-salary-AI](https://github.com/Tameralinada/simple-salary-AI)
- Issue Tracker: [https://github.com/Tameralinada/simple-salary-AI/issues](https://github.com/Tameralinada/simple-salary-AI/issues)

## 📧 Contact

If you have any questions or suggestions, please feel free to open an issue on GitHub.
