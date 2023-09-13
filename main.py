from fastapi import FastAPI, HTTPException
from test_data import *
from schemas import (
    Color,
    LegoSet,
    LegoSetWithUsersThatCanBuildIt,
    ReducedLegoSet,
    UserReduced,
    UserFull,
)
from matchings import get_sets_user_can_build, get_users_that_can_build_set

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/users")
async def get_users() -> list[UserReduced]:
    # returns a list of users in the catalogue
    return user_test_data


@app.get("/api/user/by-name/{user_name}")
async def user_summary(user_name):
    # returns a summary of a single user
    for user in user_test_data:
        if user.name == user_name:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/api/user/by-id/{user_id}")
async def user_full_data(user_id: int):
    # return the full data for a single user
    for user in user_test_data:
        if user.id == user_id:
            return UserFull(
                **user.model_dump(),
                sets=get_sets_user_can_build(user, lego_set_test_data)
            )
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/api/sets")
async def get_sets() -> list[ReducedLegoSet]:
    # returns a list of the sets in the catalogue
    return lego_set_test_data


@app.get("/api/set/by-name/{name}")
async def get_sets_by_name(name) -> LegoSet:
    # returns a summary of a single set
    for set_ in lego_set_test_data:
        if set_.name == name:
            return set_
    raise HTTPException(status_code=404, detail="Set not found")


@app.get("/api/set/by-id/{set_id}")
async def get_sets_by_id(set_id: int) -> LegoSetWithUsersThatCanBuildIt:
    # returns the full data for a single set including the users that can build it
    for set_ in lego_set_test_data:
        if set_.id == set_id:
            out = set_.model_dump()
            out["can_build"] = get_users_that_can_build_set(set_, user_test_data)
            return out
    raise HTTPException(status_code=404, detail="Set not found")


@app.get("/api/colors")
async def get_colors() -> list[Color]:
    # returns the full list of colors available
    # https://rebrickable.com/api/v3/lego/colors/?key=b4e0697ce3d5cf21af1088e9bd238dd
    # I did not have a token
    return colors_test_data
