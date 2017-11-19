app_name = "exampleApp"

# filesystem settings
out_dir = "results"
log_file = "hn_parser.log"
out_file = "report.csv"

# categories settings
categories = [
    "askstories",
    "showstories",
    "newstories",
    "jobstories"
]
default_category = "newstories"

# url settings
url_category = "https://hacker-news.firebaseio.com/v0/{{placeholder}}.json?print=pretty"
url_item = "https://hacker-news.firebaseio.com/v0/item/{{placeholder}}.json?print=pretty"

# filter settings
from_date = "2017-11-18"  # format YYYY-MM-DD
score = 0
tag = "a"   # Remove only closed tags like <p></p>
# If don't want remove tag - leave it empty: tag = ""
