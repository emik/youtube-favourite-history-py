import sqlite3
from googleapiclient.discovery import build

conn = sqlite3.connect('favourites.db')
db = conn.cursor()
db.row_factory = sqlite3.Row

oldFavourites = {}
newFavourites = {}

with open('apiKey.txt', 'r') as auth:
    apiKey = auth.readline()
with open('playlistID.txt', 'r') as auth:
    playlistID = auth.readline()

favouritesRS = db.execute("SELECT * FROM current_favourites")
for favouriteVideo in favouritesRS.fetchall():
    oldFavourites[favouriteVideo['videoID']] = favouriteVideo['videoTitle']

youtube = build(
    'youtube',
    'v3',
    developerKey=apiKey
)

def getSearchResponse(youtube, nextPageToken):
    handler = youtube.playlistItems().list(
        playlistId=playlistID,
        part="id,snippet,contentDetails",
        maxResults=50,
        pageToken=nextPageToken
    )
    print(handler.uri)
    return handler.execute()

nextPageToken = ""
searchResponse = getSearchResponse(youtube, nextPageToken)

while 'nextPageToken' in searchResponse:
    for video in searchResponse['items']:
        # ignore characters python can't interpret properly
        videoTitle = video['snippet']['title'].encode('UTF-8', 'ignore')
        videoID = video['id'].encode('UTF-8', 'ignore')
        newFavourites[videoID] = videoTitle
        # insert into difference if there is one
        if videoID in oldFavourites and videoTitle != oldFavourites[videoID]:
            db.execute(
                "INSERT INTO updated_favourites ("
                    "videoID, oldVideoTitle, newVideoTitle, dateUpdated) "
                    "VALUES(?,?,?,DATETIME())",
                    (videoID, oldFavourites[videoID], videoTitle)
            )

    searchResponse = getSearchResponse(youtube, nextPageToken)
    if 'nextPageToken' in searchResponse:
        nextPageToken = searchResponse['nextPageToken']

for videoID, videoTitle in newFavourites.items():
    db.execute("REPLACE INTO current_favourites (videoID, videoTitle) VALUES (?, ?)",
        (videoID, videoTitle)
    )

conn.commit()
conn.close()