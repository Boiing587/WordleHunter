from pydantic import BaseModel


class Attribute(BaseModel):
    name: str
    note: str | None
