from ht import *


data = {"quotes": Quotes(), "authors": Authors(), "tags": Tags()}
parse_quotes(cfg.url, data)
# aut = data.get("authors").get_all()
# a = aut[0]
# soup = get_soup(a.get("url"))
parse_authors(data)
