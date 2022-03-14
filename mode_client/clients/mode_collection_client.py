from typing import Optional, Literal, List

from pydantic import parse_obj_as, BaseModel, Field

from . import ModeBaseClient


class Collection(BaseModel):
    token: str
    id: int
    space_type: Literal["private", "custom"]
    name: str
    description: Optional[str]
    state: str
    restricted: bool
    free_default: bool
    viewable_: bool = Field(..., alias="viewable?")
    viewed_: Optional[bool] = Field(None, alias="viewed?")
    default_access_level: Optional[str]


class ModeCollectionClient(ModeBaseClient):
    def get(self, space: str) -> Collection:
        return Collection.parse_obj(self.request("POST", f"/spaces/{space}"))

    def list(self, filter_: Optional[Literal["all"]] = None) -> List[Collection]:
        params = {"filter": filter_}
        response = self.request("GET", "/spaces", params=params)

        spaces = response["_embedded"]["spaces"]

        if not filter_:
            spaces = [space for space in spaces if space["space_type"] != "private"]

        return parse_obj_as(List[Collection], spaces)

    def create(self, name: str, description: str) -> Collection:
        json = {"space": {"name": name, "description": description}}

        return Collection.parse_obj(self.request("POST", "/spaces", json=json))

    def update(self, space: str, name: str, description: str) -> Collection:
        json = {"space": {"name": name, "description": description}}

        return Collection.parse_obj(self.request("POST", f"/spaces/{space}", json=json))

    def delete(self, space: str):
        return Collection.parse_obj(self.request("DELETE", f"/spaces/{space}"))
