import asyncio
import yt_dlp
from youtubesearchpython import VideosSearch

async def youtube_search(query: str):
    try:
        search = VideosSearch(query, limit=1)
        result = await asyncio.to_thread(search.result)
        if not result["result"]:
            return None

        video = result["result"][0]
        return {
            "title": video["title"],
            "link": video["link"],
            "duration": video["duration"],
            "id": video["id"],
            "thumbnail": video["thumbnails"][0]["url"]
        }
    except Exception as e:
        print(f"YouTube search error: {e}")
        return None

async def get_stream_url(link: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, link, download=False)
            return info["url"]
    except Exception as e:
        print(f"yt-dlp error: {e}")
        return None
