import os
import asyncio
from pyrogram import filters
from pyrogram.types import Message
import yt_dlp
import config

@filters.on_message(filters.command(["song", "video"]) & filters.group)
async def song_downloader(client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply_text("Please provide a song name to download!")

    m = await message.reply_text(f"Searching for {query}...")
    is_video = message.command[0] == "video"

    ydl_opts = {
        "format": "bestaudio/best" if not is_video else "best",
        "outtmpl": "Music/cache/%(title)s.%(ext)s",
        "quiet": True,
    }

    try:
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{query}", download=True)
                if not info or not info.get("entries"):
                    return None, None
                entry = info["entries"][0]
                return entry, ydl.prepare_filename(entry)

        info, file_path = await asyncio.to_thread(download)
        if not info:
            return await m.edit("Could not find any results.")

        await m.edit("Uploading...")
        if is_video:
            await message.reply_video(file_path, caption=info["title"])
        else:
            await message.reply_audio(file_path, caption=info["title"])

        await m.delete()
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        await m.edit(f"Error: {e}")
