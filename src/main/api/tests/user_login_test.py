import pytest

from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username, 'После авторизации API вернул данные другого пользователя'
        assert response.user.role == "ROLE_ADMIN", 'Роль не совпадает с ожидаемой, ошибка!'


    def test_login_user(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username, 'Расхождение между отправленным логином и логином в ответе, ошибка!'
        assert response.user.role == "ROLE_USER", 'Роль не совпадает с ожидаемой, ошибка!'