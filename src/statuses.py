
all_text = (
	"Recently Added",
	"Favourites",
	"Reading List",
	"Dropped",
	"Completed"
)

all_ids = (0, 1, 2, 4, 5)


def text_to_id(text: str):
	return all_ids[all_text.index(text)]
