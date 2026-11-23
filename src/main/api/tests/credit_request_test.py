import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_user_request import CreateCreditUserRequest, CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, user_with_credit_account):
        initial_balance = user_with_credit_account.balance

        credit_request = CreditRequest(accountId=user_with_credit_account.id, amount=5000, termMonths=12)
        response = api_manager.user_steps.credit(create_credit_user_request, credit_request)

        assert response.balance == initial_balance + 5000

        transaction_from_db = TransactionCrudDb.get_transaction_by_receiver(
            db_session,
            account_id = user_with_credit_account.id,
            transaction_type = 'credit_issuance',
            amount = credit_request.amount
        )
        assert transaction_from_db is not None, 'Кредит не создан, ошибка!'
        assert transaction_from_db.amount == response.amount

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account_id = user_with_credit_account.id)
        assert account_from_db is not None, 'Счет не найден, Ошибка!'
        assert account_from_db.balance == response.balance



    def test_credit_request_invalid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, user_with_account):
        initial_balance = user_with_account.balance
        credit_request = CreditRequest(accountId=user_with_account.id, amount=5000, termMonths=12)
        api_manager.user_steps.credit_invalid(create_user_request, credit_request, ResponseSpecs.request_forbidden())

        transaction_from_db = TransactionCrudDb.get_transaction_by_receiver(
            db_session,
            account_id = user_with_account.id,
            transaction_type = 'credit_issuance',
            amount = credit_request.amount
        )
        assert transaction_from_db is None, 'Кредит найден, Ошибка!'

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account_id=user_with_account.id)
        assert account_from_db is not None, 'Счет не найден, Ошибка!'
        assert account_from_db.balance == initial_balance



        #
#    @pytest.mark.xfail(reason="API returns 404 instead of expected 403")
#    def test_credit_request_invalid(self, user_with_credit_account):
#        account, api_manager, create_credit_user_request = user_with_credit_account
#
#        credit_request = CreditRequest(accountId=account.id, amount=5000, termMonths=12)
#
#        api_manager.user_steps.credit(create_credit_user_request, credit_request)
#
#        api_manager.user_steps.credit_invalid(create_credit_user_request, credit_request, ResponseSpecs.request_forbidden())