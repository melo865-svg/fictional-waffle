import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.test_data.negative_test_data import NegativeTestData


@pytest.mark.api
class TestUserDeposit:
    def test_user_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, user_with_account):
        deposit_request = DepositRequest(accountId=user_with_account.id, amount=RandomModelGenerator.generate(DepositRequest).amount)
        response = api_manager.user_steps.deposit(create_user_request, deposit_request)

        assert response.balance == user_with_account.balance + deposit_request.amount, 'Баланс отличается от ожидаемого, ошибка!'

        transaction_from_db = TransactionCrudDb.get_transaction_by_receiver(
            db_session,
            account_id = user_with_account.id,
            transaction_type = 'deposit',
            amount = deposit_request.amount
        )

        assert transaction_from_db is not None, 'Депозит не обнаружен, ошибка!'
        assert transaction_from_db.amount == deposit_request.amount, 'Размер депозита отличается от запрошенного, ошибка!'


    def test_user_deposit_invalid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, user_with_account):
        deposit_request = DepositRequest(accountId=user_with_account.id, amount=NegativeTestData.below_min(DepositRequest, "amount"))
        api_manager.user_steps.deposit_invalid(create_user_request, deposit_request, ResponseSpecs.request_bad())

        transaction_from_db = TransactionCrudDb.get_transaction_by_sender(
            db_session,
            account_id = user_with_account.id,
            transaction_type = 'deposit',
            amount = deposit_request.amount
        )

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account_id = user_with_account.id)
        assert transaction_from_db is None, 'Депозит найден, ошибка!'
        assert account_from_db is not None, 'Счет не найден, ошибка!'
        assert account_from_db.balance == user_with_account.balance, 'Баланс отличается от ожидаемого, ошибка!'


