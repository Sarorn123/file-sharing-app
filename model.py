from sqlmodel import Field, SQLModel

class ImageTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename : str
    user_id : int | None
    is_public : bool | None

class UserTable(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None