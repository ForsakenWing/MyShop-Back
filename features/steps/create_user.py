from behave import given, when, then
from faker import Faker
from requests import request

fake = Faker()
url = "http://0.0.0.0:8088"


@given('User with valid data')
def get_valid_user_data(context):
    username = fake.first_name()
    password = fake.password()
    email = fake.email()
    return dict(
        username=username,
        password=password,
        email=email
    )


@when('Send request to api/v1/user/new endpoint')
def create_user(context):
    global user_data, response
    user_data = get_valid_user_data(context)
    response = request(
        method="post",
        url=f"{url}/api/v1/user/new",
        json=user_data
    )
    del user_data['password']


@then('User successfully created')
def assert_that_user_successfully_created(context):
    for key in user_data:
        assert response.json()['data']['user'][key] == user_data[key]
    assert response.status_code == 201
