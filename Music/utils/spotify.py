import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config
import re

class SpotifyAPI:
    def __init__(self):
        if config.SPOTIFY_CLIENT_ID and config.SPOTIFY_CLIENT_SECRET:
            self.client_credentials_manager = SpotifyClientCredentials(
                client_id=config.SPOTIFY_CLIENT_ID,
                client_secret=config.SPOTIFY_CLIENT_SECRET
            )
            self.spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        else:
            self.spotify = None

    def get_track_info(self, url):
        if not self.spotify:
            return None
        try:
            track = self.spotify.track(url)
            return {
                "title": f"{track['name']} - {track['artists'][0]['name']}",
                "thumbnail": track['album']['images'][0]['url']
            }
        except Exception:
            return None

    def get_album_info(self, url):
        if not self.spotify:
            return None
        try:
            album = self.spotify.album(url)
            tracks = []
            for item in album['tracks']['items']:
                tracks.append(f"{item['name']} - {item['artists'][0]['name']}")
            return {
                "title": album['name'],
                "tracks": tracks,
                "thumbnail": album['images'][0]['url']
            }
        except Exception:
            return None

    def get_playlist_info(self, url):
        if not self.spotify:
            return None
        try:
            playlist = self.spotify.playlist(url)
            tracks = []
            for item in playlist['tracks']['items']:
                track = item['track']
                tracks.append(f"{track['name']} - {track['artists'][0]['name']}")
            return {
                "title": playlist['name'],
                "tracks": tracks,
                "thumbnail": playlist['images'][0]['url']
            }
        except Exception:
            return None

spotify = SpotifyAPI()
