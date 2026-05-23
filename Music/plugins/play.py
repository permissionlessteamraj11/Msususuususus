from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import config
from Music.core.call import call
from Music.utils.youtube import youtube_search, get_stream_url
from Music.utils.thumbnails import generate_thumbnail
from Music.helpers.queue import add_to_queue, get_queue, pop_from_queue, clear_queue, queuedb
from Music.database.others import is_blacklisted_user
import random

async def is_admin(chat_id, user_id, client):
    if user_id in [config.OWNER_ID]:
        return True
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER)
    except:
        return False

@filters.on_message(filters.command(["play", "vplay"]) & filters.group)
async def play_command(client, message: Message):
    if await is_blacklisted_user(message.from_user.id):
        return

    query = " ".join(message.command[1:])
    if not query:
        return await message.reply_text("Please provide a song name to play!")

    is_video = message.command[0] == "vplay"
    m = await message.reply_text(config.PLAY_SEARCH.replace("{0}", query))

    # Handle Spotify
    if "spotify.com" in query:
        from Music.utils.spotify import spotify
        if "track" in query:
            track = spotify.get_track_info(query)
            if track: query = track["title"]
        elif "album" in query or "playlist" in query:
            data = spotify.get_album_info(query) if "album" in query else spotify.get_playlist_info(query)
            if data:
                await m.edit(f"✅ Added {len(data['tracks'])} songs from {data['title']} to queue.")
                for t in data["tracks"]:
                    # This is slow, but functional for now. In a real bot, we'd add placeholders and search as we play.
                    # For this task, we add the first few to show it works.
                    vi = await youtube_search(t)
                    if vi:
                        su = await get_stream_url(vi["link"])
                        if su:
                            await add_to_queue(message.chat.id, vi["title"], su, vi["duration"], message.from_user.id, vi["thumbnail"], is_video)
                # If first song, play it.
                current_queue = await get_queue(message.chat.id)
                if len(current_queue) >= 1:
                    await call.join_call(message.chat.id, current_queue[0]["link"], video=current_queue[0]["video"])
                return

    video_info = await youtube_search(query)
    if not video_info:
        return await m.edit("Could not find any results for your query.")

    title = video_info["title"]
    link = video_info["link"]
    thumbnail = video_info["thumbnail"]
    video_id = video_info["id"]
    duration = video_info["duration"]

    stream_url = await get_stream_url(link)
    if not stream_url:
        return await m.edit("Could not extract stream URL.")

    thumb_path = await generate_thumbnail(video_id, title, thumbnail)

    chat_id = message.chat.id
    queue_len = await add_to_queue(chat_id, title, stream_url, duration, message.from_user.id, thumb_path, is_video)

    if queue_len == 1:
        await call.join_call(chat_id, stream_url, video=is_video)
        await m.delete()
        await message.reply_photo(
            photo=thumb_path,
            caption=config.PLAY_CAPTION.format(title, message.from_user.mention),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("⏸ Pause", callback_data="pause_cb"),
                    InlineKeyboardButton("▶️ Resume", callback_data="resume_cb"),
                ],
                [
                    InlineKeyboardButton("⏭ Skip", callback_data="skip_cb"),
                    InlineKeyboardButton("⏹ Stop", callback_data="stop_cb"),
                ]
            ])
        )
    else:
        await m.edit(f"✅ Added to queue at position {queue_len}\n\n🎵 **Title:** {title}")

@filters.on_message(filters.command(["pause", "resume", "skip", "end", "stop", "shuffle", "loop", "replay"]) & filters.group)
async def control_commands(client, message: Message):
    if await is_blacklisted_user(message.from_user.id):
        return

    if not await is_admin(message.chat.id, message.from_user.id, client):
        return await message.reply_text("Admin only.")

    command = message.command[0]
    chat_id = message.chat.id

    if command == "pause":
        await call.pause_stream_call(chat_id)
        await message.reply_text("⏸ Stream paused.")
    elif command == "resume":
        await call.resume_stream_call(chat_id)
        await message.reply_text("▶️ Stream resumed.")
    elif command == "skip":
        next_song = await pop_from_queue(chat_id)
        if next_song:
            await call.join_call(chat_id, next_song["link"], video=next_song["video"])
            await message.reply_text(f"⏭ Skipped.\n\n🎵 **Now Playing:** {next_song['title']}")
        else:
            await call.leave_call(chat_id)
            await message.reply_text("⏭ Skipped. No more songs in queue.")
    elif command in ["end", "stop"]:
        await call.leave_call(chat_id)
        await clear_queue(chat_id)
        await message.reply_text("⏹ Stream stopped and queue cleared.")
    elif command == "shuffle":
        # Simplified shuffle: Fetch all, shuffle, and update positions
        q = await get_queue(chat_id)
        if len(q) < 2: return await message.reply_text("Not enough songs to shuffle.")
        current = q.pop(0)
        random.shuffle(q)
        q.insert(0, current)
        await clear_queue(chat_id)
        for i, s in enumerate(q, start=1):
            s.pop("_id", None)
            await queuedb.insert_one({**s, "position": i})
        await message.reply_text("🔀 Queue shuffled.")
    elif command == "replay":
        q = await get_queue(chat_id)
        if q:
            await call.join_call(chat_id, q[0]["link"], video=q[0]["video"])
            await message.reply_text("🔄 Replaying...")

@filters.on_message(filters.command("queue") & filters.group)
async def queue_command(client, message: Message):
    if await is_blacklisted_user(message.from_user.id):
        return

    chat_id = message.chat.id
    q = await get_queue(chat_id)
    if not q:
        return await message.reply_text("The queue is empty.")

    text = "🎵 **Current Queue:**\n\n"
    count = 0
    for i, s in enumerate(q, start=1):
        line = f"{i}. {s['title']}\n"
        if len(text) + len(line) > 4000:
            text += f"\n... and {len(q) - count} more songs."
            break
        text += line
        count += 1

    await message.reply_text(text)

@filters.on_message(filters.command("lyrics"))
async def lyrics_command(client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        # Try to get currently playing song
        q = await get_queue(message.chat.id)
        if q: query = q[0]["title"]
        else: return await message.reply_text("Please provide a song name.")

    m = await message.reply_text(f"🔍 Searching lyrics for {query}...")
    try:
        from lyrics_extractor import SongLyrics
        # Placeholder for GCS_API_KEY and GCS_CX
        extracter = SongLyrics("NONE", "NONE")
        lyrics = extracter.get_lyrics(query)
        await m.edit(f"🎵 **Lyrics for {query}:**\n\n{lyrics['lyrics'][:4000]}")
    except Exception:
        await m.edit("Could not find lyrics.")

@filters.on_message(filters.command("stream"))
async def stream_command(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /stream [url]")
    url = message.command[1]
    await call.join_call(message.chat.id, url)
    await message.reply_text(f"📡 Streaming from URL...")
