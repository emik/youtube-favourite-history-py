import sqlite3

conn = sqlite3.connect('favourites.db')
db = conn.cursor()

db.execute("CREATE TABLE current_favourites (videoID text, videoTitle text)")
db.execute("CREATE TABLE updated_favourites (videoID text, oldVideoTitle text, newVideoTitle text)")

conn.close()