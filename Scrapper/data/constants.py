import os

comicStatusPairings = (
    {"text": "Recently Added"  , "id": 0, "downloadable": True},
    {"text": "Favourites"      , "id": 1, "downloadable": True},
    {"text": "Reading List"    , "id": 2, "downloadable": True},
    {"text": "Rarely Updates"  , "id": 3, "downloadable": True},
    {"text": "Dropped"         , "id": 4, "downloadable": False},
    {"text": "Completed"       , "id": 5, "downloadable": False},
    )

comicSortPairings = (
    {"text": "Comic Title"     , "id": 0},
    {"text": "Chaps Available" , "id": 1},
    )

databasePath   = os.path.join(os.getcwd(), "data", "DB.DB")
comicOutputDir = os.path.join(os.path.expanduser("~"), "Documents", "Downloaded Media", "Comics")
