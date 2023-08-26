from pathlib import Path

from pydantic import BaseModel, Field


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
