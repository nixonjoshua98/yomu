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
	def _write_default_data(mcs):
		mcs._write_data(mcs.DEFAULT_DATA)

	@classmethod
	def _read_data(mcs) -> dict:
		with open(mcs.USER_DATA_PATH, "r") as f:
			data = json.load(f)

		return data

	@classmethod
	def _write_data(mcs, d):
		with open(mcs.USER_DATA_PATH, "w") as f:
			json.dump(d, f)

	@classmethod
	def _validate_file(mcs):
		if not os.path.isfile(mcs.USER_DATA_PATH):
			""" Log Error """

			mcs._write_default_data()

	@classmethod
	def __getattribute__(mcs, item):
		mcs._validate_file()

		data = mcs._read_data()

		if item in data:
			return data[item]

		else:
			raise AttributeError(f"{item} is not in the user data")

	@classmethod
	def __setattr__(mcs, item, val):
		raise Exception("Setattr has been disabled")

		mcs._validate_file()

		data = mcs._read_data()

		if item in data:
			data[item] = val
			mcs._write_data(data)

		else:
			raise AttributeError(f"{item} is not in the user data")


class UserData(metaclass=UserDataMeta):
	pass
