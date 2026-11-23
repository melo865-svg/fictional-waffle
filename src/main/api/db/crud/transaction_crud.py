from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_transaction_by_sender(db: Session, account_id: int, transaction_type: str, amount: float) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=account_id, transaction_type=transaction_type, amount=amount).first()

    @staticmethod
    def get_transaction_by_receiver(db: Session, account_id: int, transaction_type: str, amount: float) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=account_id, transaction_type=transaction_type, amount=amount).first()

    @staticmethod
    def get_transactions_by_receiver(db: Session, account_id: int) -> list[Transaction]:
        return db.query(Transaction).filter_by(to_account_id=account_id).all()