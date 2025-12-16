from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from ..models.transaction import Transaction, TransactionType
from ..models.monthly_summary import MonthlySummary
from decimal import Decimal

class TransactionService:
    @staticmethod
    def create_transaction(db: Session, user_id: int, transaction_data: dict):
        transaction = Transaction(
            user_id=user_id,
            **transaction_data
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        # Update monthly summary
        TransactionService.update_monthly_summary(db, user_id, transaction.date)
        return transaction

    @staticmethod
    def get_user_transactions(db: Session, user_id: int, limit: int = 50):
        return db.query(Transaction).filter(
            Transaction.user_id == user_id
        ).order_by(Transaction.date.desc()).limit(limit).all()

    @staticmethod
    def get_dashboard_data(db: Session, user_id: int, year: int, month: int):
        # Get monthly totals
        income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.INCOME,
            extract('year', Transaction.date) == year,
            extract('month', Transaction.date) == month
        ).scalar() or Decimal('0')

        expenses = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.EXPENSE,
            extract('year', Transaction.date) == year,
            extract('month', Transaction.date) == month
        ).scalar() or Decimal('0')

        # Category breakdown
        categories = db.query(
            Transaction.category,
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.EXPENSE,
            extract('year', Transaction.date) == year,
            extract('month', Transaction.date) == month
        ).group_by(Transaction.category).all()

       # Category breakdown income
        categories_income = db.query(
            Transaction.category,
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.INCOME,
            extract('year', Transaction.date) == year,
            extract('month', Transaction.date) == month
        ).group_by(Transaction.category).all()

        return {
            'income': float(income),
            'expenses': float(expenses),
            'savings': float(income - expenses),
            'category_breakdown': [
                {'category': cat.category, 'amount': float(cat.total)}
                for cat in categories
            ],
            'category_breakdown_income': [
                {'category': cat.category, 'amount': float(cat.total)}
                for cat in categories_income
            ]
        }

    @staticmethod
    def update_monthly_summary(db: Session, user_id: int, date):
        year, month = date.year, date.month
        
        summary = db.query(MonthlySummary).filter(
            MonthlySummary.user_id == user_id,
            MonthlySummary.year == year,
            MonthlySummary.month == month
        ).first()

        if not summary:
            summary = MonthlySummary(user_id=user_id, year=year, month=month)
            db.add(summary)

        # Recalculate totals
        income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.INCOME,
            extract('year', Transaction.date) == year,
            extract('month', Transaction.date) == month
        ).scalar() or Decimal('0')

        expenses = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.EXPENSE,
            extract('year', Transaction.date) == year,
            extract('month', Transaction.date) == month
        ).scalar() or Decimal('0')

        summary.total_income = income
        summary.total_expenses = expenses
        summary.savings = income - expenses
        
        db.commit()