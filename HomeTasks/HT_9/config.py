import os


APP_NAME = "exampleApp"

# filesystem settings
OUT_DIR = "results"
LOG_FILE = OUT_DIR + os.sep + "hn_parser.log"
OUT_FILE = OUT_DIR + os.sep + "{datestamp}.html"

# categories settings
CATEGORIES = [
    "topstories",
    "newstories",
    "beststories",
    "askstories",
    "showstories",
    "jobstories"
]
DEFAULT_CATEGORY = "all"

# url settings
url_category = "https://hacker-news.firebaseio.com/v0/{cat}.json?print=pretty"
url_item = "https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty"

# filter settings
from_date = "2017-11-18"  # format YYYY-MM-DD
score = 0
tag = "a"   # Remove only closed tags like <p></p>
# If don't want remove tag - leave it empty: tag = ""
