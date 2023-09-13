from schemas import User, LegoSet


def can_build(inventory, lego_set):
    return all(
        piece.match_id in inventory
        and inventory[piece.match_id].quantity >= piece.quantity
        for piece in lego_set.piece_sets
    )


def get_sets_user_can_build(user: User, lego_sets: list[LegoSet]):
    inventory = {piece.match_id: piece for piece in user.piece_sets}
    return [set_ for set_ in lego_sets if can_build(inventory, set_)]


def get_users_that_can_build_set(lego_set, users):
    return [user for user in users if get_sets_user_can_build(user, [lego_set])]
