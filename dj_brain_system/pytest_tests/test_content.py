import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    'name',
    (
        'common_pages:feedback',
        'questions:questions',
        'questions:add',
    )
)
def test_page_contains_form(admin_client, name):
    """
    Проверка наличия формы в словаре контекста ответа для страниц,
    на которых должна отображаться форма.
    """
    url = reverse(name)
    response = admin_client.get(url)
    assert response.context.get('form') is not None, (
        f'На странице по адресу {url} не отображается форма.'
    )


@pytest.mark.django_db
def test_file_response(client):
    """
    Проверка наличия файла в ответе.
    """
    url = reverse('brain_system:export_model_to_ods')
    response = client.get(url)
    assert list(response.streaming_content) != [], (
        f'В ответ на запрос к адресу {url} не был возвращен файл.'
    )


@pytest.mark.django_db
def test_bought_in_products_page(
    client, bought_in_product,
    bought_in_product_as_a_part_of,
    bought_in_product_link
):
    """
    Проверка наличия данных о деталях в контексте ответа.
    """
    url = reverse('brain_system:bought')
    response = client.get(url)
    object_list = response.context['object_list']
    assert bought_in_product in object_list, (
        f'В ответе на запрос к адресу {url} нет объекта BoughtInProduct.'
    )
    assert object_list[0].a_part_of == bought_in_product_as_a_part_of, (
        'В поле "a_part_of" объекта BoughtInProduct отсутствует'
        ' объект BoughtInProductAsAPartOf.'
    )
    assert object_list[0].a_part_of.name == 'Блок_1', (
        'Содержимое поля "name" объекта BoughtInProductAsAPartOf'
        ' не соответствует ожидаемому.'
    )
    assert object_list[0].name == 'Деталь_1', (
        'Содержимое поля "name" объекта BoughtInProduct'
        ' не соответствует ожидаемому.'
    )
    links = object_list[0].link_for_product.all()
    assert links[0].product == bought_in_product, (
        'Поле "product" объекта BoughtInProductLink не содержит'
        'объекта BoughtInProduct'
    )
    assert links[1].product == bought_in_product, (
        'Поле "product" объекта BoughtInProductLink не содержит'
        'объекта BoughtInProduct'
    )
    assert links[0].link == 'https://example1.com', (
        'Содержимое поля "link" объекта BoughtInProductLink'
        ' не соответствует ожидаемому.'
    )
    assert links[1].link_short_name == 'example2', (
        'Содержимое поля "link_short_name" объекта BoughtInProductLink'
        ' не соответствует ожидаемому.'
    )


@pytest.mark.django_db
def test_generate_rand_questions(client, question_form_data, question_set):
    """
    Проверка наличия данных о деталях в контексте ответа.
    """
    url = reverse('questions:questions')
    response = client.post(url, data=question_form_data)
    assert 'queryset' in response.context, (
        'Запрос на вывод случайных вопросов не возвращает'
        ' сгенерированные вопросы'
    )
    assert 'page_obj' in response.context, (
        'Запрос на вывод случайных вопросов не возвращает'
        ' информацию о пагинации сгенерированных вопросов.'
    )
    assert (len(response.context['queryset'])
            == int(question_form_data['questions_quantity'])), (
        'Общее количество сгенерированных случайных вопросов'
        ' не соответствует ожидаемому.'
    )
    assert (len(response.context['page_obj'])
            == int(question_form_data['questions_displayed_on_page'])), (
        'Количество сгенерированных случайных вопросов, отображаемое '
        'на странице, не соответствует ожидаемому.'
    )
