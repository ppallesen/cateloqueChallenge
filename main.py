from fastapi import FastAPI, HTTPException
from data_directory import *
from schemas import (
    Color,
    LegoSet,
    LegoSetWithUsersThatCanBuildIt,
    ReducedLegoSet,
    UserReduced,
    UserFull,
    PieceSet,
)
from matchings import (
    find_users_that_can_help_complete_the_set,
    get_sets_user_can_build,
    get_users_that_can_build_set,
)
from find_largest_set import find_largest_possible_set_that_most_can_build

app = FastAPI()


@app.get("/api/users")
async def get_users() -> list[UserReduced]:
    # returns a list of users in the catalogue
    return user_test_data


@app.get("/api/user/by-name/{user_name}")
async def user_summary(user_name) -> User:
    # returns a summary of a single user
    return find_or_raise_error(user_test_data, user_name, "name")


@app.get("/api/user/by-id/{user_id}")
async def user_full_data(user_id: int) -> UserFull:
    # return the full data for a single user
    user = find_or_raise_error(user_test_data, user_id)
    return UserFull(
        **user.model_dump(), sets=get_sets_user_can_build(user, lego_set_test_data)
    )


@app.get("/api/sets")
async def get_sets() -> list[ReducedLegoSet]:
    # returns a list of the sets in the catalogue
    return lego_set_test_data


@app.get("/api/set/by-name/{name}")
async def get_sets_by_name(name) -> LegoSet:
    # returns a summary of a single set
    return find_or_raise_error(lego_set_test_data, name, "name")


@app.get("/api/collaborators")
async def get_collaborators(user_id: int, set_id: int) -> list[UserReduced]:
    # Returns the users the user can collaborate with in order to finish the set
    # If the user can finish the set them self the api fails. So call only this API
    # for sets that the user cannot build them self.
    user = find_or_raise_error(user_test_data, user_id)
    set_ = find_or_raise_error(lego_set_test_data, set_id)
    return find_users_that_can_help_complete_the_set(set_, user, user_test_data)


@app.get("/api/set/by-id/{set_id}")
async def get_sets_by_id(set_id: int) -> LegoSetWithUsersThatCanBuildIt:
    # returns the full data for a single set including the users that can build it
    set_ = find_or_raise_error(lego_set_test_data, set_id)
    out = set_.model_dump()
    out["can_build"] = get_users_that_can_build_set(set_, user_test_data)
    return out


@app.get("/api/colors")
async def get_colors() -> list[Color]:
    # returns the full list of colors available
    # Considered using https://rebrickable.com/api/v3/lego/colors/?key=b4e0697ce3d5cf21af1088e9bd238dd
    # I did not have a token
    return colors_test_data


@app.get("/api/find-largest-set")
async def get_largest_set(p: float) -> list[PieceSet]:
    # returns the largest possible set that can be created, where p of the users
    # can build it, where p is a ratio e.g. 0.5

    return [
        PieceSet(piece_id=piece_id, material_id=material_id, quantity=quantity)
        for (
            piece_id,
            material_id,
        ), quantity in find_largest_possible_set_that_most_can_build(
            user_test_data, p
        ).items()
    ]


def find_or_raise_error(collection: list, value, field="id"):
    for item in collection:
        if getattr(item, field) == value:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
