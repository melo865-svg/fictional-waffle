import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_user_request import CreateCreditUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, user_with_active_credit):
        initial_balance = user_with_active_credit.balance
        credit_repay_request = CreditRepayRequest(creditId=user_with_active_credit.creditId, accountId=user_with_active_credit.id, amount=user_with_active_credit.amount)
        response = api_manager.user_steps.credit_repay(create_credit_user_request, credit_repay_request)

        assert response.amountDeposited == credit_repay_request.amount

        transaction_from_db = TransactionCrudDb.get_transaction_by_receiver(
            db_session,
            account_id = user_with_active_credit.id,
            transaction_type = 'credit_issuance',
            amount = credit_repay_request.amount
        )

        assert transaction_from_db is not None, 'Выплата не обнаружена, Ошибка'
        assert transaction_from_db.to_account_id == user_with_active_credit.id

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account_id=user_with_active_credit.id)

        assert account_from_db is not None, 'Счет не обнаружен, ошибка'
        assert account_from_db.balance == initial_balance - credit_repay_request.amount

    def test_credit_repay_invalid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, user_with_credit_account, user_with_active_credit, user_with_balance_and_payed_credit):

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account_id=user_with_credit_account.id)
        assert account_from_db is not None, 'Счет не обнаружен, ошибка!'

        initial_balance = account_from_db.balance

        transactions_before = TransactionCrudDb.get_transactions_by_receiver(db_session, user_with_credit_account.id)

        credit_repay_request = CreditRepayRequest(creditId=user_with_balance_and_payed_credit.creditId, accountId=user_with_credit_account.id, amount=user_with_active_credit.amount)
        api_manager.user_steps.credit_repay_invalid(create_credit_user_request, credit_repay_request, ResponseSpecs.request_conflict())

        transactions_after = TransactionCrudDb.get_transactions_by_receiver(db_session, user_with_credit_account.id)

        db_session.refresh(account_from_db)

        assert len(transactions_before) == len(transactions_after)
        assert account_from_db.balance == initial_balance




       # #credit_repay_request = CreditRepayRequest(creditId=user_with_active_credit.creditId, accountId=user_with_active_credit.id, amount=3500)
#
        #api_manager.user_steps.credit_repay_invalid(create_credit_user_request, credit_repay_request, ResponseSpecs.request_unprocessable_entity())
