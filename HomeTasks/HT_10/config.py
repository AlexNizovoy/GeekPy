import os


APP_NAME = "HackerNewsParser"

# filesystem settings
OUT_DIR = "results"
LOG_FILE = OUT_DIR + os.sep + "hn_parser.log"
OUT_FILE = OUT_DIR + os.sep + "hn_parser_{datestamp}.html"
STORAGE_FILE = OUT_DIR + os.sep + "storage.pkl"

# Database settings
DB_HOST = "localhost"
DB_HOST_PORT = 5432
DB_NAME = "hn_parser"
DB_USER = "postgres"
DB_PASS = "1595159"

# categories settings
CATEGORIES = [
    "topstories",
    "newstories",
    "beststories",
    "askstories",
    "showstories",
    "jobstories",
]
DEFAULT_CATEGORY = "all"

# url settings
url_category = "https://hacker-news.firebaseio.com/v0/{}.json?print=pretty"
url_item = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty"

# filter settings
from_date = "2018-01-01"  # format YYYY-MM-DD
score = 0
tag = "a"   # Remove only closed tags like <p></p>
# If don't want remove tag - leave it empty: tag = ""
