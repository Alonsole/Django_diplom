import pytest
from django.urls import reverse
from rest_framework import status
from backend.models import User
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()


TEST_USER = {
        'first_name': 'Test',
        'last_name': 'Tests',
        'password': 'Qwert@_12345',
        'company': 'CompanyTest',
        'position': 'Director',
    }
email = 'test123456789@mail.ru'
url_yaml = 'https://raw.githubusercontent.com/bku4erov/py-diplom/master/data/shop1.yaml'


@pytest.mark.django_db
class TestUser:
    """регистрация юзера"""
    def test_registration(self, api_client):
        test_user = {'email': email, **TEST_USER}
        response = api_client.post(reverse('backend:user-register'), test_user)
        # проверка статус кода
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert response_json.get('Status') == True
        # проверка записи БД
        created_user = User.objects.get(email=test_user['email'])
        assert created_user
        # проверка полей
        test_user.pop('password')
        for test_user_field in test_user.keys():
            assert getattr(created_user, test_user_field) == test_user[test_user_field]


    def test_create_account_missing_field(self, api_client):
        """регистрация без обязательного поля"""
        response = api_client.post(reverse('backend:user-register'), **TEST_USER)
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert response_json.get('Status') == False
        assert 'Errors' in response_json
        assert 'Не указаны все необходимые аргументы' in response_json['Errors']