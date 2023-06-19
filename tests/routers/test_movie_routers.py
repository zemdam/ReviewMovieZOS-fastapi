import pytest
from json import dumps
from .test_other_route import add_all, SAMPLE_COUNTRY, SAMPLE_GENRE

SAMPLE_MOVIE = [
    {
        "title": "Sample title",
        "genre_name": "Action",
        "release_date": "2001-06-06",
        "description": "Sample description",
        "country_name": "Poland",
    },
    {
        "title": "Sample title2",
        "genre_name": "Action",
        "release_date": "2006-03-06",
        "description": "Sample description2",
        "country_name": "France",
    },
    {
        "title": "Sample title3",
        "genre_name": "Drama",
        "release_date": "2022-03-09",
        "description": "Sample description3",
        "country_name": "France",
    },
]

SAMPLE_REVIEW = [
    {
        "rating": 4,
        "description": "Sample description",
        "user_name": "Adam2023",
    },
    {
        "rating": 7,
        "user_name": "Adam2023",
    },
    {
        "rating": 3,
        "description": "Bad movie",
        "user_name": "Watcher12",
    },
]


@pytest.mark.parametrize("movie", SAMPLE_MOVIE)
def test_add_movie(client, movie, add_all):
    response = client.post("movie/", content=dumps(movie))
    assert response.status_code == 200
    movie_copy = movie.copy()
    movie_copy["id"] = response.json()["id"]
    movie_copy["rating"] = 0
    movie_copy["number_of_ratings"] = 0
    assert response.json() == movie_copy


@pytest.mark.parametrize("country", SAMPLE_COUNTRY)
def test_get_movies_from_country(client, country, add_all):
    added = []
    for movie in SAMPLE_MOVIE:
        response = client.post("movie/", content=dumps(movie))
        assert response.status_code == 200
        if movie["country_name"] == country["name"]:
            added.append(response.json())
        response = client.get("movies/?country=" + country["name"])
        assert response.status_code == 200
        for added_movie in added:
            assert added_movie in response.json()
        assert len(response.json()) == len(added)


@pytest.mark.parametrize("genre", SAMPLE_GENRE)
def test_get_movies_from_genre(client, genre, add_all):
    added = []
    for movie in SAMPLE_MOVIE:
        response = client.post("movie/", content=dumps(movie))
        assert response.status_code == 200
        if movie["genre_name"] == genre["name"]:
            added.append(response.json())
        response = client.get("movies/?genre=" + genre["name"])
        assert response.status_code == 200
        for added_movie in added:
            assert added_movie in response.json()
        assert len(response.json()) == len(added)


@pytest.mark.parametrize("country", SAMPLE_COUNTRY)
@pytest.mark.parametrize("genre", SAMPLE_GENRE)
def test_get_movies_from_genre(client, genre, country, add_all):
    added = []
    for movie in SAMPLE_MOVIE:
        response = client.post("movie/", content=dumps(movie))
        assert response.status_code == 200
        if (
            movie["genre_name"] == genre["name"]
            and movie["country_name"] == country["name"]
        ):
            added.append(response.json())
        response = client.get(
            "movies/?genre=" + genre["name"] + "&country=" + country["name"]
        )
        assert response.status_code == 200
        for added_movie in added:
            assert added_movie in response.json()
        assert len(response.json()) == len(added)


def add_review(client, review, movie_id=1):
    response = client.post(f"/movie/{movie_id}/review", content=dumps(review))
    assert response.status_code == 200
    review_copy = review.copy()
    review_copy["id"] = response.json()["id"]
    review_copy["movie_id"] = movie_id
    if "description" not in review_copy:
        review_copy["description"] = None
    assert response.json() == review_copy


@pytest.mark.parametrize("review", SAMPLE_REVIEW)
def test_add_review(client, review, add_all, movie_id=1):
    test_add_movie(client, SAMPLE_MOVIE[0], add_all)
    add_review(client, review, movie_id)
    response = client.get("movie/" + str(movie_id))
    assert review["rating"] == response.json()["rating"]
    assert response.json()["number_of_ratings"] == 1


@pytest.mark.parametrize("movie", SAMPLE_MOVIE)
def test_add_multiple_review(client, movie, add_all, movie_id=1):
    avg = 0
    test_add_movie(client, movie, add_all)
    for review in SAMPLE_REVIEW:
        avg += review["rating"]
        add_review(client, review, movie_id)
    avg /= len(review)
    response = client.get("movie/" + str(movie_id))
    assert avg == response.json()["rating"]
    assert len(review) == response.json()["number_of_ratings"]


@pytest.mark.parametrize("movie", SAMPLE_MOVIE)
def test_get_reviews(client, movie, add_all):
    test_add_multiple_review(client, movie, add_all)
    response = client.get("movie/1/reviews")
    assert len(response.json()) == len(SAMPLE_REVIEW)


def test_top_movies(client, add_all, limit=2):
    test_add_multiple_review(client, SAMPLE_MOVIE[1], add_all, movie_id=1)
    test_add_review(client, SAMPLE_REVIEW[0], add_all, movie_id=2)
    response = client.get("movies/top?limit=" + str(limit))
    assert len(response.json()) == 2
    response_json = response.json()
    assert response_json[0]["rating"] >= response_json[1]["rating"]
    assert response_json[0]["rating"] == (4 + 7 + 3) / 3
    assert response_json[1]["rating"] == 4


def test_top_movies(client, add_all, limit=1):
    test_add_multiple_review(client, SAMPLE_MOVIE[1], add_all, movie_id=1)
    test_add_review(client, SAMPLE_REVIEW[0], add_all, movie_id=2)
    response = client.get("movies/top?limit=" + str(limit))
    assert len(response.json()) == 1
    response_json = response.json()
    assert response_json[0]["rating"] == (4 + 7 + 3) / 3
