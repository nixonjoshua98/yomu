from src.updateworker import UpdateWorker

from src.application import Application

if __name__ == "__main__":
	app = Application()

	UpdateWorker(app.data_storage).start()

	app.mainloop()
