TRACK_TERMS = ["NFL", "seahawks", "fantasy football", "seattle"]
CONNECTION_STRING = "sqlite:///tweets.db"
CSV_NAME = "tweets.csv"
TABLE_NAME = "nfl"

try:
    from private import *
except Exception:
    pass
