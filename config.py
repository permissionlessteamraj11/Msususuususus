import os
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv(".env")

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
LOGGER_ID = int(os.getenv("LOGGER_ID", "-100"))
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
STRING_SESSION = os.getenv("STRING_SESSION")

OWNER_USERNAME = os.getenv("OWNER_USERNAME", "The_LuckyX")
BOT_USERNAME = os.getenv("BOT_USERNAME", "PritiMusicBot")
BOT_NAME = os.getenv("BOT_NAME", "PritiMusic")
ASSUSERNAME = os.getenv("ASSUSERNAME", "PritiMusic")

SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/PritiSupport")
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/PritiSupportChat")

UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/TheLuckyX/PritiMusic")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "main")

MUST_JOIN = os.getenv("MUST_JOIN", "PritiSupport")

DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "60"))
AUTO_LEAVING_ASSISTANT = os.getenv("AUTO_LEAVING_ASSISTANT", "True")
ASSISTANT_LEAVE_TIME = int(os.getenv("ASSISTANT_LEAVE_TIME", "5400"))

SONG_DOWNLOAD_DURATION = int(os.getenv("SONG_DOWNLOAD_DURATION", "180"))
SONG_DOWNLOAD_DURATION_LIMIT = int(os.getenv("SONG_DOWNLOAD_DURATION_LIMIT", "180"))
PLAYLIST_FETCH_LIMIT = int(os.getenv("PLAYLIST_FETCH_LIMIT", "25"))

TG_AUDIO_FILESIZE_LIMIT = int(os.getenv("TG_AUDIO_FILESIZE_LIMIT", "104857600"))
TG_VIDEO_FILESIZE_LIMIT = int(os.getenv("TG_VIDEO_FILESIZE_LIMIT", "1073741824"))

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

START_CAPTION = os.getenv("START_CAPTION", "✨ Welcome to **PritiMusic**\n\nA premium music bot with neon orange style.")
PLAY_CAPTION = os.getenv("PLAY_CAPTION", "🎵 **Now Playing:** {0}\n👤 **Requested by:** {1}")
PLAY_SEARCH = os.getenv("PLAY_SEARCH", "🔍 Searching for {0}...")
SUPPORT_CAPTION = os.getenv("SUPPORT_CAPTION", "💬 Contact support if you have issues.")
REPO_CAPTION = os.getenv("REPO_CAPTION", "📦 Source code of PritiMusic.")

EFFECT_IDS = os.getenv("EFFECT_IDS", "5159385139981059251").split()

START_URL = os.getenv("START_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
HELP_URL = os.getenv("HELP_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
PLAY_URL = os.getenv("PLAY_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
SUPPORT_URL = os.getenv("SUPPORT_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
REPO_URL = os.getenv("REPO_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
PING_URL = os.getenv("PING_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
PLAYLIST_URL = os.getenv("PLAYLIST_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
STATS_URL = os.getenv("STATS_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")

TELEGRAM_AUDIO_URL = os.getenv("TELEGRAM_AUDIO_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
TELEGRAM_VIDEO_URL = os.getenv("TELEGRAM_VIDEO_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
STREAM_URL = os.getenv("STREAM_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
SOUNDCLOUD_URL = os.getenv("SOUNDCLOUD_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
YOUTUBE_URL = os.getenv("YOUTUBE_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
SPOTIFY_ARTIST_URL = os.getenv("SPOTIFY_ARTIST_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
SPOTIFY_ALBUM_URL = os.getenv("SPOTIFY_ALBUM_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
SPOTIFY_PLAYLIST_URL = os.getenv("SPOTIFY_PLAYLIST_URL", "https://graph.org/file/0c9e62f6b3e979d5069b2.jpg")
