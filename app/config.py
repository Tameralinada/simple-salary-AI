CATEGORIES = ['Essential', 'Luxury', 'Salary', 'Investments', 'Services']

# German tax rates (simplified for demonstration)
GERMANY_TAX_RATES = {
    "income": 0.42,  # 42% income tax rate
    "VAT_standard": 0.19,  # 19% standard VAT
    "VAT_reduced": 0.07,  # 7% reduced VAT
}

# Budget category allocations (percentage of after-tax income)
BUDGET_CATEGORIES = {
    "Essential": {
        "percentage": 50,
        "description": "Basic needs like food, housing, utilities",
        "subcategories": ["Groceries", "Rent", "Utilities", "Transportation"]
    },
    "Savings": {
        "percentage": 20,
        "description": "Emergency fund and long-term savings",
        "subcategories": ["Emergency Fund", "Retirement", "Investment"]
    },
    "Discretionary": {
        "percentage": 30,
        "description": "Non-essential spending and entertainment",
        "subcategories": ["Entertainment", "Dining Out", "Shopping", "Hobbies"]
    }
}

# Social security contributions (percentage of gross income)
SOCIAL_SECURITY = {
    "health_insurance": 7.3,  # Public health insurance
    "pension_insurance": 9.3,  # Pension insurance
    "unemployment_insurance": 1.2,  # Unemployment insurance
    "nursing_care_insurance": 1.525  # Nursing care insurance
}
