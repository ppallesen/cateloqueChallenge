from schemas import PieceSet, User, LegoSet

colors_test_data = [
    {"hex_color": "#FF0000", "name": "red", "material_id": 1},
    {"hex_color": "#0000FF", "name": "blue", "material_id": 2},
]

piece_sets = [
    PieceSet(piece_id=1, material_id=1, quantity=2),
    PieceSet(piece_id=1, material_id=1, quantity=1),
    PieceSet(piece_id=1, material_id=2, quantity=2),
    PieceSet(piece_id=2, material_id=1, quantity=2),
]

user_test_data = [
    User(id=0, name="brickfan35", piece_sets=[piece_sets[1], piece_sets[2]]),
    User(id=1, name="landscape-artis", piece_sets=[piece_sets[1], piece_sets[3]]),
    User(id=2, name="megabuilder99", piece_sets=[piece_sets[1]]),
    User(id=3, name="dr_crocodile", piece_sets=[piece_sets[3]]),
]
lego_set_test_data = [
    LegoSet(
        id=1,
        name="tropical-island",
        piece_sets=[piece_sets[0], piece_sets[2], piece_sets[3]],
    ),
    LegoSet(id=2, name="first-set", piece_sets=[piece_sets[1]]),
]
