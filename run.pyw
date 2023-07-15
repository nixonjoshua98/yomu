from src.models.app_config import AppConfig
from src.updateworker import UpdateWorker
from pathlib import Path

from src.application import Application

if __name__ == "__main__":
	config = AppConfig.read_from_file(Path(__file__).with_name("config.json"))

	app = Application(config)

	UpdateWorker(app.data_storage).start()

	app.mainloop()
