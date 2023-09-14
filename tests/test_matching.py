from data_directory import *
from matchings import (
    find_users_that_can_help_complete_the_set,
    get_sets_user_can_build,
    get_users_that_can_build_set,
    find_missing_pieces,
)
from conftest import rng_string


def test_user_cant_build_a_set_if_there_is_not_match_on_material():
    set_ = LegoSet(
        id=1,
        name=rng_string(),
        piece_sets=[PieceSet(piece_id=1, material_id=1, quantity=2)],
    )
    user = User(
        id=0,
        name=rng_string(),
        piece_sets=[PieceSet(piece_id=1, material_id=2, quantity=2)],
    )
    assert get_sets_user_can_build(user, [set_]) == []


def test_user_cant_build_a_set_if_the_quantity_is_too_low():
    set_ = LegoSet(
        id=1,
        name=rng_string(),
        piece_sets=[PieceSet(piece_id=1, material_id=1, quantity=2)],
    )
    user = User(
        id=0,
        name=rng_string(),
        piece_sets=[PieceSet(piece_id=1, material_id=1, quantity=1)],
    )
    assert get_sets_user_can_build(user, [set_]) == []


def test_user_can_build_a_set_even_if_there_are_too_many_bricks():
    set_ = LegoSet(
        id=1,
        name=rng_string(),
        piece_sets=[PieceSet(piece_id=1, material_id=1, quantity=2)],
    )
    user = User(
        id=0,
        name=rng_string(),
        piece_sets=[PieceSet(piece_id=1, material_id=1, quantity=3)],
    )
    assert get_sets_user_can_build(user, [set_]) == [set_]


def test_user_cant_build_a_set_even_if_the_user_has_half_of_the_brick_types():
    set_ = LegoSet(
        id=1,
        name=rng_string(),
        piece_sets=[
            PieceSet(piece_id=1, material_id=1, quantity=2),
            PieceSet(piece_id=1, material_id=3, quantity=1),
        ],
    )
    user = User(
        id=0,
        name=rng_string(),
        piece_sets=[PieceSet(piece_id=1, material_id=1, quantity=4)],
    )
    assert get_sets_user_can_build(user, [set_]) == []


def test_find_users_to_complete_the_set_does_not_find_main_user():
    set_ = LegoSet(
        id=1,
        name=rng_string(),
        piece_sets=[
            PieceSet(piece_id=1, material_id=1, quantity=2),
        ],
    )
    main_user = User(
        id=0,
        name=rng_string(),
        piece_sets=[PieceSet(piece_id=1, material_id=1, quantity=1)],
    )
    assert find_users_that_can_help_complete_the_set(set_, main_user, [main_user]) == []


def test_find_users_that_can_be_used_to_combine_set():
    set_ = LegoSet(
        id=1,
        name=rng_string(),
        piece_sets=[
            PieceSet(piece_id=1, material_id=1, quantity=2),
            PieceSet(piece_id=2, material_id=1, quantity=2),
        ],
    )
    main_user = User(
        id=0,
        name=rng_string(),
        piece_sets=[PieceSet(piece_id=1, material_id=1, quantity=1)],
    )
    user_that_matches = User(
        id=1,
        name=rng_string(),
        piece_sets=[
            PieceSet(piece_id=1, material_id=1, quantity=1),
            PieceSet(piece_id=2, material_id=1, quantity=2),
        ],
    )
    users_that_does_not_have_all_needed = [
        User(
            id=2,
            name=rng_string(),
            piece_sets=[PieceSet(piece_id=2, material_id=1, quantity=2)],
        ),
        User(
            id=3,
            name=rng_string(),
            piece_sets=[PieceSet(piece_id=1, material_id=1, quantity=1)],
        ),
    ]
    users = [
        main_user,
        user_that_matches,
    ] + users_that_does_not_have_all_needed
    users_that_matches = find_users_that_can_help_complete_the_set(
        set_, main_user, users
    )
    assert users_that_matches == [user_that_matches], [
        user.id for user in users_that_matches
    ]


def test_find_missing_pieces():
    user_piece_sets = [
        PieceSet(piece_id=1, material_id=1, quantity=2),
        PieceSet(piece_id=2, material_id=1, quantity=1),
        PieceSet(piece_id=1, material_id=2, quantity=2),
    ]
    lego_set_pieces = [
        PieceSet(piece_id=1, material_id=1, quantity=1),
        PieceSet(piece_id=2, material_id=1, quantity=2),
        PieceSet(piece_id=3, material_id=2, quantity=2),
    ]
    missing_pieces = find_missing_pieces(user_piece_sets, lego_set_pieces)
    assert len(missing_pieces) == 2
    missing_piece_1, missing_piece_2 = sorted(missing_pieces, key=lambda x: x.match_id)
    assert missing_piece_1.model_dump() == {
        "piece_id": 2,
        "material_id": 1,
        "quantity": 1,
    }
    assert missing_piece_2.model_dump() == {
        "piece_id": 3,
        "material_id": 2,
        "quantity": 2,
    }


def test_that_users_that_build_set_and_sets_that_can_be_build_by_user_are_consistent_with_each_other():
    for set_ in lego_set_test_data:
        users_that_can_build_set = get_users_that_can_build_set(set_, user_test_data)
        for user in user_test_data:
            assert (user in users_that_can_build_set) == (
                set_ in get_sets_user_can_build(user, lego_set_test_data)
            )
