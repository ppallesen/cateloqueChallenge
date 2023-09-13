from __future__ import annotations
from pydantic import BaseModel


class PieceSet(BaseModel):
    piece_id: int
    material_id: int
    quantity: int

    @property
    def match_id(self):
        return (self.piece_id, self.material_id)


class ReducedLegoSet(BaseModel):
    id: int
    name: str


class LegoSet(ReducedLegoSet):
    piece_sets: list[PieceSet]


class Color(BaseModel):
    hex_color: str
    name: str
    material_id: int


class UserReduced(BaseModel):
    id: int
    name: str


class User(UserReduced):
    piece_sets: list[PieceSet]


class UserFull(User):
    sets: list[LegoSet]


class LegoSetWithUsersThatCanBuildIt(LegoSet):
    can_build: list[UserReduced]
