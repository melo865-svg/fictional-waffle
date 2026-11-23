from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest, CreateCreditUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response


    def deposit(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(deposit_request)
        return response

    def deposit_invalid(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest, response_spec):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT,
            response_spec
        ).post(deposit_request)

    def transfer(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_ok()
        ).post(transfer_request)
        return response

    def transfer_invalid(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest, response_spec):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER,
            response_spec
        ).post(transfer_request)
        return response

    def credit(self, create_user_request: CreateCreditUserRequest, credit_request: CreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT,
            ResponseSpecs.request_created()
        ).post(credit_request)
        return response

    def credit_invalid(self, create_user_request: CreateCreditUserRequest, credit_request: CreditRequest, response_spec):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT,
            response_spec
        ).post(credit_request)
        return response

    def credit_repay(self, create_user_request: CreateCreditUserRequest, credit_repay_request: CreditRepayRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request)
        return response

    def credit_repay_invalid(self, create_user_request: CreateCreditUserRequest, credit_repay_request: CreditRepayRequest, response_spec):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            response_spec
        ).post(credit_repay_request)
        return response