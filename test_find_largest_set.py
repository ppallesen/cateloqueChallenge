from schemas import User, PieceSet
from test_app import rng_string
from find_largest_set import find_largest_possible_set_that_most_can_build


def test_find_largest_set():
    """
    This is a very complicated test (too complicated probably). The example has multiple properties
    There are 5 users:
    - There exists no set all the users can't collect
    - The set that 4 people can collect are 1 of piece_id = 1 ( All pieces have same material_id)
    - There are multiple sets that 3 people can build, but the only one with 2 pieces is 2 of piece_id = 2
    - 2 people has the optimal build as 5 of piece_id = 3
    - with 1 person the person with most pieces have 6 of piece_id = 3 and 2 of piece_id=2
    - Using 0.5 returns the same as 0.4
    """
    users = [
        User(
            id=0,
            name=rng_string(),
            piece_sets=[PieceSet(piece_id=1, material_id=1, quantity=1)],
        ),
        User(
            id=1,
            name=rng_string(),
            piece_sets=[
                PieceSet(piece_id=1, material_id=1, quantity=2),
                PieceSet(piece_id=2, material_id=1, quantity=2),
            ],
        ),
        User(
            id=2,
            name=rng_string(),
            piece_sets=[
                PieceSet(piece_id=1, material_id=1, quantity=2),
                PieceSet(piece_id=2, material_id=1, quantity=2),
            ],
        ),
        User(
            id=3,
            name=rng_string(),
            piece_sets=[
                PieceSet(piece_id=1, material_id=1, quantity=1),
                PieceSet(piece_id=3, material_id=1, quantity=5),
            ],
        ),
        User(
            id=4,
            name=rng_string(),
            piece_sets=[
                PieceSet(piece_id=3, material_id=1, quantity=6),
                PieceSet(piece_id=2, material_id=1, quantity=2),
            ],
        ),
    ]
    assert find_largest_possible_set_that_most_can_build(users, 1) == {}
    assert find_largest_possible_set_that_most_can_build(users, 0.8) == {(1, 1): 1}
    assert find_largest_possible_set_that_most_can_build(users, 0.6) == {(2, 1): 2}
    assert find_largest_possible_set_that_most_can_build(users, 0.4) == {(3, 1): 5}
    assert find_largest_possible_set_that_most_can_build(users, 0.5) == {(3, 1): 5}
    assert find_largest_possible_set_that_most_can_build(users, 0.2) == {
        (3, 1): 6,
        (2, 1): 2,
    }
