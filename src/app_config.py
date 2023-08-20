from pathlib import Path

from pydantic import BaseModel as _BaseModel
from pydantic import Field


class BaseModel(_BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    def dict(self, *args, **kwargs):
        kwargs["by_alias"] = True

        return super().dict(**kwargs)


class EmailSenderModel(BaseModel):
    email_address: str = Field(..., alias="emailAddress")
    password: str


class AppConfig(BaseModel):
    email_sender: EmailSenderModel = Field(..., alias="emailSender")
    email_receiver: str = Field(..., alias="emailReceiver")
    database_path: str = Field(..., alias="databasePath")

    @staticmethod
    def read_from_file(file_path: Path):
        with file_path.open("r") as fh:
            data = fh.read()

        return AppConfig.parse_raw(data)
