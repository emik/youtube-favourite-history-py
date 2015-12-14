# Python Youtube Favourites History
A small script I made to track the video titles for videos that were deleted (and learn a bit of python). I was getting very frustrated with not knowing what music videos I had previously liked enough to favourite, that were now just "Deleted".

The first time it runs, the script populates current_favourites. Every time thereafter, it theoretically checks any video title differences and adds them to updated_favourites with the date the script updated it, the previous title, and the new title. I plan to use this to track any new titles with "deleted" in and find the music elsewhere.

You need an API key for accessing the Youtube Data API v3. Drop it into apiKey.txt. You will also need to drop the playlist ID into playlistID.txt.

Then just run "python main.py"

Sometimes I get a 500 response from the API which cuts the script short.