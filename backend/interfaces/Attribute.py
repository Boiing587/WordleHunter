from pydantic import BaseModel

class Attribute(BaseModel):
    name: str
    icon: str
    note: str | None