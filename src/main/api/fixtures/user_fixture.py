import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest, CreateCreditUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_credit_user(user_request)
    return user_request




@pytest.fixture
def user_with_account(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)



@pytest.fixture
def user_with_credit_account(api_manager, create_credit_user_request):
    return api_manager.user_steps.create_account(create_credit_user_request)



@pytest.fixture
def accounts_with_balance(api_manager):
    def _create_user_with_balance(amount):
        user_request = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(user_request)

        account = api_manager.user_steps.create_account(user_request)

        deposit_request = DepositRequest(accountId=account.id, amount=amount)
        deposit = api_manager.user_steps.deposit(user_request, deposit_request)

        return user_request, account, deposit

    sender = _create_user_with_balance(5000)
    receiver = _create_user_with_balance(2000)

    return sender, receiver



@pytest.fixture
def user_with_active_credit(api_manager, user_with_credit_account, create_credit_user_request):
    credit_request = RandomModelGenerator.generate(CreditRequest, accountId=user_with_credit_account.id)
    return api_manager.user_steps.credit(create_credit_user_request, credit_request)




@pytest.fixture
def user_with_balance_and_payed_credit(api_manager, user_with_active_credit, user_with_credit_account, create_credit_user_request):
    credit_repay_request = CreditRepayRequest(creditId=user_with_active_credit.creditId, accountId=user_with_credit_account.id, amount=user_with_active_credit.amount)
    deposit_request = DepositRequest(accountId=user_with_credit_account.id, amount=min(user_with_active_credit.amount, 9000))
    api_manager.user_steps.deposit(create_credit_user_request, deposit_request)

    if user_with_active_credit.amount > deposit_request.amount:
        deposit_request_1 = DepositRequest(accountId=user_with_credit_account.id, amount=user_with_active_credit.amount - deposit_request.amount)
        api_manager.user_steps.deposit(create_credit_user_request, deposit_request_1)

    return api_manager.user_steps.credit_repay(create_credit_user_request, credit_repay_request)