import pytest
from json import dumps

SAMPLE_COUNTRY = [
    {
        "name": "Poland",
    },
    {
        "name": "Spain",
    },
    {"name": "France"},
]

SAMPLE_GENRE = [
    {
        "name": "Action",
    },
    {
        "name": "Comedy",
    },
    {
        "name": "Drama",
    },
]

SAMPLE_USER = [
    {
        "name": "Adam2023",
    },
    {
        "name": "Watcher12",
    },
    {
        "name": "flash00",
    },
]


def check_equal(json1, json2):
    assert len(json1) == len(json2)
    for key in json1:
        assert key in json2


@pytest.mark.parametrize("country", SAMPLE_COUNTRY)
def test_add_country(client, country):
    response = client.post("other/country", content=dumps(country))
    assert response.status_code == 200
    assert response.json()["name"] == country["name"]


def test_no_countries(client):
    response = client.get("other/countries")
    assert response.status_code == 200
    assert response.json() == []


def test_all_countries(client):
    for country in SAMPLE_COUNTRY:
        test_add_country(client, country)
    response = client.get("other/countries")
    assert response.status_code == 200
    check_equal(response.json(), SAMPLE_COUNTRY)


@pytest.mark.parametrize("genre", SAMPLE_GENRE)
def test_add_genre(client, genre):
    response = client.post("other/genre", content=dumps(genre))
    assert response.status_code == 200
    assert response.json()["name"] == genre["name"]


def test_no_genres(client):
    response = client.get("other/genres")
    assert response.status_code == 200
    assert response.json() == []


def test_all_genres(client):
    for genre in SAMPLE_GENRE:
        test_add_genre(client, genre)
    response = client.get("other/genres")
    assert response.status_code == 200
    check_equal(response.json(), SAMPLE_GENRE)


@pytest.mark.parametrize("user", SAMPLE_USER)
def test_add_user(client, user):
    response = client.post("other/user", content=dumps(user))
    assert response.status_code == 200
    assert response.json()["name"] == user["name"]


def test_no_users(client):
    response = client.get("other/users")
    assert response.status_code == 200
    assert response.json() == []


def test_all_users(client):
    for user in SAMPLE_USER:
        test_add_user(client, user)
    response = client.get("other/users")
    assert response.status_code == 200
    check_equal(response.json(), SAMPLE_USER)


@pytest.fixture
def add_all(client):
    for genre in SAMPLE_GENRE:
        test_add_genre(client, genre)
    for country in SAMPLE_COUNTRY:
        test_add_country(client, country)
    for user in SAMPLE_USER:
        test_add_user(client, user)
