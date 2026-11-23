import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestUserTransfer:
    def test_user_transfer(self, db_session: Session, api_manager: ApiManager, accounts_with_balance):
        (sender_request, sender_account, sender_deposit),\
        (receiver_request, receiver_account, receiver_deposit) = accounts_with_balance

        transfer_request = TransferRequest(fromAccountId=sender_account.id, toAccountId=receiver_account.id, amount=1500)
        transfer_response = api_manager.user_steps.transfer(sender_request, transfer_request)

        assert transfer_response.fromAccountIdBalance == sender_deposit.balance - transfer_request.amount


        transaction_from_db = TransactionCrudDb.get_transaction_by_sender(
            db_session,
            account_id = sender_account.id,
            transaction_type = 'transfer',
            amount = transfer_request.amount
        )

        assert transaction_from_db is not None, 'Перевод не найден, ошибка'
        assert transaction_from_db.to_account_id == receiver_account.id


        account_from_db_1 = AccountCrudDb.get_account_by_id(db_session, account_id = sender_account.id)

        assert account_from_db_1 is not None, 'Счет не найден, ошибка'
        assert account_from_db_1.balance == sender_deposit.balance - transfer_request.amount

        account_from_db_2 = AccountCrudDb.get_account_by_id(db_session, account_id = receiver_account.id)

        assert account_from_db_2 is not None, 'Счет не найден, ошибка'
        assert account_from_db_2.balance == receiver_deposit.balance + transfer_request.amount




    def test_user_transfer_invalid(self, db_session: Session, api_manager: ApiManager, accounts_with_balance):
        (sender_request, sender_account, sender_deposit), \
        (receiver_request, receiver_account, receiver_deposit) = accounts_with_balance


        transfer_request = TransferRequest(fromAccountId=sender_account.id, toAccountId=receiver_account.id, amount=499)
        api_manager.user_steps.transfer_invalid(sender_request, transfer_request, ResponseSpecs.request_bad())

        transaction_from_db = TransactionCrudDb.get_transaction_by_sender(
            db_session,
            account_id=sender_account.id,
            transaction_type='transfer',
            amount=transfer_request.amount
        )

        assert transaction_from_db is None, 'Перевод выполнен, ошибка!'

        account_from_db_1 = AccountCrudDb.get_account_by_id(db_session, account_id=sender_account.id)

        assert account_from_db_1 is not None, 'Счет не найден, ошибка!'
        assert account_from_db_1.balance == sender_deposit.balance

        account_from_db_2 = AccountCrudDb.get_account_by_id(db_session, account_id=receiver_account.id)

        assert account_from_db_2 is not None, 'Счет не найден, ошибка!'
        assert account_from_db_2.balance == receiver_deposit.balance








        #api_manager, accounts = create_accounts(create_user_request, count=2)
        #first_account, second_account = accounts
#
        #deposit_request = DepositRequest(accountId=first_account.id, amount=5000)
        #api_manager.user_steps.deposit(create_user_request, deposit_request)
#
        #transfer_request = TransferRequest(fromAccountId=first_account.id, toAccountId=second_account.id, amount=15000)
        #api_manager.user_steps.transfer_invalid(create_user_request, transfer_request,ResponseSpecs.request_bad())
#
       # transfer_request_1 = TransferRequest(fromAccountId=first_account.id, toAccountId=second_account.id, amount=5001)
       # api_manager.user_steps.transfer_invalid(create_user_request, transfer_request_1, ResponseSpecs.request_unprocessable_entity())

