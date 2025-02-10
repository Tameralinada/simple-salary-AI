from . import db
from datetime import datetime
import json

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'date': self.date,
            'category': self.category,
            'tax_rate': self.tax_rate,
            'tax_amount': self.tax_amount
        }

class BudgetSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    monthly_limit = db.Column(db.Float, nullable=False)
    alert_threshold = db.Column(db.Float, nullable=False)  # Percentage (0-100)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'monthly_limit': self.monthly_limit,
            'alert_threshold': self.alert_threshold,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
