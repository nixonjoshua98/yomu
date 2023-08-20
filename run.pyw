from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app_config import AppConfig
from src.update_worker import UpdateWorker
from pathlib import Path
from src.application import Application
from src.data_repository import DataRepository
from src.data_entities import Base


def initialize_database(file_path: str) -> DataRepository:

    engine = create_engine(file_path)

    Base.metadata.create_all(engine)

    session_maker = sessionmaker()

    session_maker.configure(bind=engine)

    return DataRepository(session_maker)


if __name__ == "__main__":
    config = AppConfig.read_from_file(Path(__file__).with_name("config.json"))

    repository = initialize_database(config.database_path)

    app = Application(config, repository)

    UpdateWorker(repository).start()

    app.mainloop()
