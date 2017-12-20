APP_NAME = "exampleApp"

# filesystem settings
OUT_DIR = "results"
LOG_FILE = "hn_parser.log"
OUT_FILE = "report.csv"

# categories settings
CATEGORIES = [
    "askstories",
    "showstories",
    "newstories",
    "jobstories"
]
DEFAULT_CATEGORY = "newstories"

# url settings
url_category = "https://hacker-news.firebaseio.com/v0/{{placeholder}}.json?print=pretty"
url_item = "https://hacker-news.firebaseio.com/v0/item/{{placeholder}}.json?print=pretty"

# filter settings
from_date = "2017-11-18"  # format YYYY-MM-DD
score = 0
tag = "a"   # Remove only closed tags like <p></p>
# If don't want remove tag - leave it empty: tag = ""
