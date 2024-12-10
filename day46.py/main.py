from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# User input for date
date = input(
    "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
)

# Scrape Billboard Hot 100
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
}
url = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(url=url, headers=header)

# Check if the response was successful
if response.status_code != 200:
    print(
        "Failed to retrieve Billboard data. Please check the date format or your connection."
    )
    exit()

soup = BeautifulSoup(response.text, "html.parser")
# Select song titles based on the current structure of the Billboard website
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

if not song_names:
    print(
        "Could not extract song names. The Billboard website structure might have changed."
    )
    exit()

print(f"Scraped {len(song_names)} songs from Billboard Hot 100.")

# Authenticate with Spotify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.getenv("Client_ID"),
        client_secret=os.getenv("Client_secret"),
        show_dialog=True,
        cache_path="token.txt",
    )
)
# Get user ID
user_id = sp.current_user()["id"]

# Search for songs on Spotify
song_uris = []
year = date.split("-")[0]

for song in song_names:
    try:
        result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        print(f"Found: {song}")
    except (IndexError, KeyError):
        print(f"Skipped: {song} - Not found on Spotify.")
    time.sleep(1)  # Avoid hitting API rate limits

# Create a Spotify playlist
if song_uris:
    playlist_name = f"Billboard Hot 100 - {date}"
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    sp.user_playlist_add_tracks(
        user=user_id, playlist_id=playlist["id"], tracks=song_uris
    )
    print(
        f"Playlist created successfully! You can find it here: {playlist['external_urls']['spotify']}"
    )
else:
    print(
        "No songs were added to the playlist. Please check your inputs and try again."
    )
