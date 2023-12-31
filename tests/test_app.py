from data_directory import *
from matchings import (
    get_sets_user_can_build,
    get_users_that_can_build_set,
)
import json
from conftest import client, rng_string


def test_get_colors():
    response = client.get("/api/colors")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert data[0]["hex_color"] == colors_test_data[0]["hex_color"]
    assert data[0]["material_id"] == colors_test_data[0]["material_id"]


def test_get_sets_by_name():
    set_ = lego_set_test_data[0]
    response = client.get(f"/api/set/by-name/{set_.name}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == set_.id
    assert len(data["piece_sets"]) == len(set_.piece_sets)
    assert "can_build" not in data


def test_get_set_by_name_fails_in_a_good_way_if_wrong_name_is_provided():
    response = client.get(f"/api/set/by-name/{rng_string()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_all_sets_can_be_fetched_and_all_the_pieces_are_not_included_in_that_case():
    response = client.get(f"/api/sets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(lego_set_test_data)
    for item, test_data in zip(data, lego_set_test_data):
        assert item["name"] == test_data.name
        assert item["id"] == test_data.id
        assert "piece_sets" not in item


def test_get_user_by_summary_by_name():
    user = user_test_data[0]
    response = client.get(f"/api/user/by-name/{user.name}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["name"] == user.name
    assert data["piece_sets"]
    for return_piece_set, piece_set in zip(data["piece_sets"], user.piece_sets):
        assert return_piece_set["material_id"] == piece_set.material_id
        assert return_piece_set["piece_id"] == piece_set.piece_id
        assert return_piece_set["quantity"] == piece_set.quantity
        assert "match_id" not in return_piece_set
    assert "can_build" not in data


def test_get_users_and_see_that_their_collection_is_not_returned():
    response = client.get(f"/api/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(user_test_data)
    for item, test_data in zip(data, user_test_data):
        assert item["name"] == test_data.name
        assert item["id"] == test_data.id
        assert "piece_sets" not in item


def test_user_get_by_id_also_returns_sets_the_user_can_build():
    user = [
        user
        for user in user_test_data
        if get_sets_user_can_build(user, lego_set_test_data)
    ][
        0
    ]  # finding a user that can build a set
    response = client.get(f"/api/user/by-id/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user.name
    assert data["piece_sets"]
    assert data["sets"] == [
        json.loads(set_.model_dump_json())
        for set_ in get_sets_user_can_build(user, lego_set_test_data)
    ]


def test_get_set_information_by_id_get_all_information_including_all_the_users_that_can_build_it():
    set_ = [
        set_
        for set_ in lego_set_test_data
        if get_users_that_can_build_set(set_, user_test_data)
    ][
        0
    ]  # finding a set that can be built by some users
    response = client.get(f"/api/set/by-id/{set_.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == set_.name
    assert data["piece_sets"]
    for user_data, user in zip(
        data["can_build"], get_users_that_can_build_set(set_, user_test_data)
    ):
        assert user_data["name"] == user.name
        assert list(user_data.keys()) == ["id", "name"]


def test_missing_pieces_can_be_fetched_by_api():
    set_ = [set_ for set_ in lego_set_test_data if set_.name == "tropical-island"][0]
    main_user = [user for user in user_test_data if user.name == "landscape-artist"][0]
    assert set_ not in get_sets_user_can_build(main_user, lego_set_test_data)
    response = client.get(f"/api/collaborators?user_id={main_user.id}&set_id={set_.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(item["name"] == "brickfan35" for item in data)
    assert all("piece_sets" not in item for item in data)


def test_good_error_is_thrown_if_user_can_build_a_set_without_help_and_help_is_requested():
    for set_ in lego_set_test_data:
        if get_users_that_can_build_set(set_, user_test_data):
            user = get_users_that_can_build_set(set_, user_test_data)[0]
            response = client.get(
                f"/api/collaborators?user_id={user.id}&set_id={set_.id}"
            )
            assert response.status_code == 418
            assert (
                response.json()["detail"]
                == "The user can build the set without help. Please check it before you call"
            )

            return
    assert False, "No user that build a set in mock data"
