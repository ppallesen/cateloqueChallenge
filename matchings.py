from schemas import User, LegoSet, PieceSet
from fastapi import HTTPException


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


def find_missing_pieces(
    pieces_to_match_from: list[PieceSet], pieces_to_match: list[PieceSet]
):
    match_dict = {piece.match_id: piece for piece in pieces_to_match_from}
    out = []
    placeholder_match_piece = PieceSet(piece_id=-1, material_id=-1, quantity=0)
    for piece in pieces_to_match:
        match_piece = match_dict.get(piece.match_id, placeholder_match_piece)
        if match_piece.quantity < piece.quantity:
            data = piece.model_dump()
            data["quantity"] = piece.quantity - match_piece.quantity
            out.append(PieceSet(**data))
    return out


def find_users_that_can_help_complete_the_set(
    set_: LegoSet, main_user: User, users: list[User]
):
    missing_pieces = find_missing_pieces(main_user.piece_sets, set_.piece_sets)
    if not missing_pieces:
        # This exception since there is no meaningfull answer
        raise HTTPException(
            status_code=418,
            detail="The user can build the set without help. Please check it before you call",
        )

    placeholder_lego_set = LegoSet(id=-1, name="", piece_sets=missing_pieces)
    return get_users_that_can_build_set(
        placeholder_lego_set, [user for user in users if user.id != main_user.id]
    )
