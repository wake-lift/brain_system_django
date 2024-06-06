from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name', (
        'common_pages:main',
        'common_pages:legal',
        'common_pages:feedback',
        'brain_system:operating',
        'brain_system:circuit',
        'brain_system:pcb',
        'brain_system:printed',
        'brain_system:bought',
        'brain_system:firmware',
        'brain_system:export_model_to_ods',
        'questions:questions',
        'questions:tg-bot',
        'login',
        'password_reset',
        'registration',
    )
)
def test_pages_availability_for_anon_user(client, name):
    """
    Проверка статуса ответа 200 для анонимного пользователя
    от общедоступных страниц.
    """
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'Обращение от анонимного пользователя к адресу {url} '
        'возвращает статус ответа, отличный от 200.'
    )


@pytest.mark.parametrize(
    'name', (
        'questions:add',
    )
)
def test_pages_availability_for_auth_user(admin_client, name):
    """
    Проверка статуса ответа 200 для аутентифицированного пользователя от
    страниц, требующих аутентификации.
    """
    url = reverse(name)
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'Обращение от аутентифицированного пользователя к адресу {url} '
        'возвращает статус ответа, отличный от 200.'
    )


@pytest.mark.parametrize(
    'name, name_redirect', (
        ('questions:add', 'login'),
    )
)
def test_pages_redirect_to_login_for_anon_user(client, name, name_redirect):
    """
    Проверка перенаправления на страницу аутентификации для анономного
    пользователя от страниц, требующих аутентификации.
    """
    expected_url = f'{reverse(name_redirect)}?next={reverse(name)}'
    response = client.get(reverse(name))
    assertRedirects(
        response,
        expected_url,
        msg_prefix=(
            f'Обращение от анонимного пользователя к адресу {reverse(name)} '
            'не возвращает редирект на страницу аутентификации.'
        )
    )
