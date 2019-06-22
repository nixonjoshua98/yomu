import os
import json


class UserDataMeta(type):
	USER_DATA_PATH = os.path.join(os.getcwd(), "..", "Data", "user_data.json")

	DEFAULT_DATA = {
		"manga_save_dir": r"D:\Downloaded Media\Comics",
		"database_path": r"D:\OneDrive - UoL\OneDrive - University of Lincoln\manga_database.sqlite3",
		"database_con_str": "sqlite:///"
	}

	@classmethod
	def _write_default_data(cls):
		cls._write_data(cls.DEFAULT_DATA)

	@classmethod
	def _read_data(cls) -> dict:
		with open(cls.USER_DATA_PATH, "r") as f:
			data = json.load(f)

		return data

	@classmethod
	def _write_data(cls, d):
		with open(cls.USER_DATA_PATH, "w") as f:
			json.dump(d, f)

	@classmethod
	def _validate_file(cls):
		if not os.path.isfile(cls.USER_DATA_PATH):
			""" Log Error """

			cls._write_default_data()

	@classmethod
	def __getattribute__(cls, item):
		cls._validate_file()

		data = cls._read_data()

		if item in data:
			return data[item]

		else:
			raise AttributeError(f"{item} is not in the user data")

	@classmethod
	def __setattr__(cls, item, val):
		raise Exception("Setattr has been disabled")

		cls._validate_file()

		data = cls._read_data()

		if item in data:
			data[item] = val
			cls._write_data(data)

		else:
			raise AttributeError(f"{item} is not in the user data")


class UserData(metaclass=UserDataMeta):
	pass
