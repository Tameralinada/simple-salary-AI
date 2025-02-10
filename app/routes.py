from flask import Blueprint, request, jsonify, render_template, send_file
from datetime import datetime, timedelta
import pandas as pd
import io
import csv
from .models import Transaction, BudgetSetting
from . import db
from .config import CATEGORIES, GERMANY_TAX_RATES, BUDGET_CATEGORIES, SOCIAL_SECURITY

main = Blueprint('main', __name__)

def simple_classify(description):
    # Simple keyword-based classification
    description = description.lower()
    if any(word in description for word in ['grocery', 'groceries', 'food', 'supermarket', 'lidl', 'aldi', 'edeka', 'rewe']):
        return 'Essential'
    elif any(word in description for word in ['restaurant', 'dinner', 'lunch', 'cinema', 'entertainment', 'cafe', 'bar']):
        return 'Luxury'
    elif any(word in description for word in ['salary', 'wage', 'income', 'payment']):
        return 'Salary'
    elif any(word in description for word in ['investment', 'stock', 'bond', 'dividend']):
        return 'Investments'
    else:
        return 'Services'

def calculate_german_tax(category, amount):
    if category == "Salary" or category == "Investments":
        return amount * GERMANY_TAX_RATES["income"]
    elif category == "Luxury" or category == "Services":
        return amount * GERMANY_TAX_RATES["VAT_standard"]
    else:
        return amount * GERMANY_TAX_RATES["VAT_reduced"]

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/classify_transaction', methods=['POST'])
def classify_transaction():
    try:
        print("Received transaction classification request")
        data = request.json
        print(f"Request data: {data}")
        
        description = data['description']
        amount = float(data['amount'])
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"Classifying transaction: {description}")
        category = simple_classify(description)
        print(f"Classification result: {category}")
        
        tax_amount = calculate_german_tax(category, amount)
        tax_rate = (tax_amount / amount) * 100 if amount > 0 else 0.0
        
        new_transaction = Transaction(
            description=description,
            amount=amount,
            date=date,
            category=category,
            tax_rate=tax_rate,
            tax_amount=tax_amount
        )
        db.session.add(new_transaction)
        db.session.commit()
        print("Transaction saved successfully")
        
        return jsonify({
            'message': 'Transaction categorized and saved', 
            'category': category, 
            'tax_amount': tax_amount
        })
    except Exception as e:
        print(f"Error in classify_transaction: {str(e)}")
        return jsonify({'error': str(e)}), 400

@main.route('/analytics/spending_by_category', methods=['GET'])
def spending_by_category():
    try:
        # Get date range from query parameters
        days = request.args.get('days', default=30, type=int)
        start_date = datetime.now() - timedelta(days=days)
        
        # Query transactions
        transactions = Transaction.query.filter(
            Transaction.date >= start_date.strftime("%Y-%m-%d")
        ).all()
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame([{
            'amount': t.amount,
            'category': t.category,
            'date': datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S")
        } for t in transactions])
        
        if df.empty:
            return jsonify({
                'categories': [],
                'amounts': [],
                'percentages': []
            })
        
        # Calculate spending by category
        category_totals = df[df['category'] != 'Salary'].groupby('category')['amount'].sum()
        total_spending = category_totals.sum()
        percentages = (category_totals / total_spending * 100).round(2)
        
        return jsonify({
            'categories': category_totals.index.tolist(),
            'amounts': category_totals.values.tolist(),
            'percentages': percentages.values.tolist()
        })
    except Exception as e:
        print(f"Error in spending_by_category: {str(e)}")
        return jsonify({'error': str(e)}), 400

@main.route('/analytics/monthly_trends', methods=['GET'])
def monthly_trends():
    try:
        # Get last 6 months of data
        start_date = datetime.now() - timedelta(days=180)
        
        # Query transactions
        transactions = Transaction.query.filter(
            Transaction.date >= start_date.strftime("%Y-%m-%d")
        ).all()
        
        # Convert to DataFrame
        df = pd.DataFrame([{
            'amount': t.amount,
            'category': t.category,
            'date': datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S")
        } for t in transactions])
        
        if df.empty:
            return jsonify({
                'labels': [],
                'income': [],
                'expenses': []
            })
        
        # Add month column
        df['month'] = df['date'].dt.strftime('%Y-%m')
        
        # Calculate monthly income and expenses
        monthly_income = df[df['category'] == 'Salary'].groupby('month')['amount'].sum()
        monthly_expenses = df[df['category'] != 'Salary'].groupby('month')['amount'].sum()
        
        # Get all months in range
        all_months = pd.date_range(
            start=df['date'].min(),
            end=df['date'].max(),
            freq='M'
        ).strftime('%Y-%m').tolist()
        
        # Fill in missing months with 0
        monthly_income = monthly_income.reindex(all_months, fill_value=0)
        monthly_expenses = monthly_expenses.reindex(all_months, fill_value=0)
        
        return jsonify({
            'labels': all_months,
            'income': monthly_income.values.tolist(),
            'expenses': monthly_expenses.values.tolist()
        })
    except Exception as e:
        print(f"Error in monthly_trends: {str(e)}")
        return jsonify({'error': str(e)}), 400

@main.route('/transactions', methods=['GET'])
def get_transactions():
    try:
        print("Fetching all transactions")
        
        # Get filter parameters
        category = request.args.get('category', default=None)
        start_date = request.args.get('start_date', default=None)
        end_date = request.args.get('end_date', default=None)
        min_amount = request.args.get('min_amount', default=None, type=float)
        max_amount = request.args.get('max_amount', default=None, type=float)
        
        # Start with base query
        query = Transaction.query
        
        # Apply filters
        if category:
            query = query.filter(Transaction.category == category)
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if min_amount is not None:
            query = query.filter(Transaction.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Transaction.amount <= max_amount)
        
        transactions = query.all()
        return jsonify([t.to_dict() for t in transactions])
    except Exception as e:
        print(f"Error in get_transactions: {str(e)}")
        return jsonify({'error': str(e)}), 400

@main.route('/financial_insights', methods=['POST'])
def financial_insights():
    try:
        print("Received financial insights request")
        data = request.json
        question = data['question']
        print(f"Question: {question}")
        
        # Simple response without ollama
        response = f"I understand you're asking about: {question}. However, the AI-powered insights feature requires the Ollama package to be properly installed and configured."
        print("Sending simple response")
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in financial_insights: {str(e)}")
        return jsonify({'error': str(e)}), 400

@main.route('/budget/set', methods=['POST'])
def set_budget():
    try:
        data = request.json
        category = data['category']
        monthly_limit = float(data['monthly_limit'])
        alert_threshold = float(data['alert_threshold'])

        # Update or create budget setting
        budget = BudgetSetting.query.filter_by(category=category).first()
        if budget:
            budget.monthly_limit = monthly_limit
            budget.alert_threshold = alert_threshold
        else:
            budget = BudgetSetting(
                category=category,
                monthly_limit=monthly_limit,
                alert_threshold=alert_threshold
            )
            db.session.add(budget)
        
        db.session.commit()
        return jsonify({'message': f'Budget set for {category}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/budget/status', methods=['GET'])
def get_budget_status():
    try:
        # Get current month's start date
        today = datetime.now()
        month_start = today.replace(day=1).strftime("%Y-%m-%d")
        
        # Get all budget settings
        budgets = BudgetSetting.query.all()
        status = []
        
        for budget in budgets:
            # Get total spending for the category this month
            transactions = Transaction.query.filter(
                Transaction.category == budget.category,
                Transaction.date >= month_start,
                Transaction.category != 'Salary'
            ).all()
            
            total_spent = sum(t.amount for t in transactions)
            percentage_used = (total_spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0
            
            status.append({
                'category': budget.category,
                'monthly_limit': budget.monthly_limit,
                'spent': total_spent,
                'remaining': budget.monthly_limit - total_spent,
                'percentage_used': percentage_used,
                'alert_threshold': budget.alert_threshold,
                'alert': percentage_used >= budget.alert_threshold
            })
        
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/export/transactions', methods=['GET'])
def export_transactions():
    try:
        format = request.args.get('format', 'csv')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build query
        query = Transaction.query
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
            
        transactions = query.all()
        
        if format == 'csv':
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(['Date', 'Description', 'Amount', 'Category', 'Tax Rate', 'Tax Amount'])
            
            # Write data
            for t in transactions:
                writer.writerow([
                    t.date,
                    t.description,
                    t.amount,
                    t.category,
                    t.tax_rate,
                    t.tax_amount
                ])
            
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'transactions_{datetime.now().strftime("%Y%m%d")}.csv'
            )
            
        elif format == 'excel':
            df = pd.DataFrame([t.to_dict() for t in transactions])
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Transactions', index=False)
                
                # Get workbook and add formats
                workbook = writer.book
                worksheet = writer.sheets['Transactions']
                
                # Add currency format
                money_fmt = workbook.add_format({'num_format': '€#,##0.00'})
                percent_fmt = workbook.add_format({'num_format': '0.00%'})
                
                # Apply formats to columns
                worksheet.set_column('C:C', 12, money_fmt)  # Amount
                worksheet.set_column('E:E', 10, percent_fmt)  # Tax Rate
                worksheet.set_column('F:F', 12, money_fmt)  # Tax Amount
                
                # Adjust column widths
                for idx, col in enumerate(df.columns):
                    worksheet.set_column(idx, idx, max(len(col) + 2, 12))
            
            output.seek(0)
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=f'transactions_{datetime.now().strftime("%Y%m%d")}.xlsx'
            )
        
        else:
            return jsonify({'error': 'Unsupported format'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/calculate_income', methods=['POST'])
def calculate_income():
    try:
        data = request.json
        gross_income = float(data['gross_income'])
        
        # Calculate social security contributions
        social_security_total = sum(SOCIAL_SECURITY.values())
        social_security_amount = (gross_income * social_security_total) / 100
        
        # Calculate income tax
        taxable_income = gross_income - social_security_amount
        income_tax = taxable_income * GERMANY_TAX_RATES["income"]
        
        # Calculate net income
        net_income = gross_income - social_security_amount - income_tax
        
        # Calculate budget allocations
        budget_allocations = {}
        for category, details in BUDGET_CATEGORIES.items():
            amount = (net_income * details["percentage"]) / 100
            budget_allocations[category] = {
                "amount": round(amount, 2),
                "percentage": details["percentage"],
                "description": details["description"],
                "subcategories": {
                    subcat: round(amount / len(details["subcategories"]), 2)
                    for subcat in details["subcategories"]
                }
            }
        
        return jsonify({
            "gross_income": round(gross_income, 2),
            "deductions": {
                "social_security": {
                    "total": round(social_security_amount, 2),
                    "details": {
                        name: round((gross_income * rate) / 100, 2)
                        for name, rate in SOCIAL_SECURITY.items()
                    }
                },
                "income_tax": round(income_tax, 2)
            },
            "net_income": round(net_income, 2),
            "budget_allocations": budget_allocations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
