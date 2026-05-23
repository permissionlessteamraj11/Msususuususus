from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import config

@filters.on_callback_query(filters.regex("help_callback"))
async def help_callback(_, query: CallbackQuery):
    await query.message.edit_caption(
        caption="✨ **PritiMusic Help Menu**\n\nClick the buttons below to see commands.",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Music Controls", callback_data="music_help"),
                InlineKeyboardButton("Admin Panel", callback_data="admin_help"),
            ],
            [
                InlineKeyboardButton("Premium Features", callback_data="premium_help"),
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="start_callback")
            ]
        ])
    )

@filters.on_callback_query(filters.regex("start_callback"))
async def start_callback(_, query: CallbackQuery):
    await query.message.edit_caption(
        caption=config.START_CAPTION,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("➕ Add Me To Your Group", url=f"https://t.me/{config.BOT_USERNAME}?startgroup=true"),
            ],
            [
                InlineKeyboardButton("🛠 Help & Commands", callback_data="help_callback"),
            ],
            [
                InlineKeyboardButton("📢 Channel", url=config.SUPPORT_CHANNEL),
                InlineKeyboardButton("💬 Support", url=config.SUPPORT_CHAT),
            ],
            [
                InlineKeyboardButton("👤 Owner", url=f"https://t.me/{config.OWNER_USERNAME}"),
            ]
        ])
    )

@filters.on_callback_query(filters.regex("music_help"))
async def music_help(_, query: CallbackQuery):
    text = """
🎵 **Music Commands:**
- /play [song name]: Play a song from YouTube
- /vplay [video name]: Play a video from YouTube
- /pause: Pause the current stream
- /resume: Resume the paused stream
- /skip: Skip to the next song in queue
- /stop: Stop the stream and clear queue
- /queue: Show the current queue
"""
    await query.message.edit_caption(
        caption=text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="help_callback")]])
    )

@filters.on_callback_query(filters.regex("admin_help"))
async def admin_help(_, query: CallbackQuery):
    text = """
📊 **Admin Commands:**
- /stats: Show bot statistics
- /broadcast: Broadcast message to all users
- /addpremium: Add premium user
- /rmpremium: Remove premium user
- /blacklist: Blacklist a user
- /whitelist: Whitelist a user
"""
    await query.message.edit_caption(
        caption=text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="help_callback")]])
    )

@filters.on_callback_query(filters.regex("premium_help"))
async def premium_help(_, query: CallbackQuery):
    text = """
✨ **Premium Features:**
- Higher audio quality
- No playback limits
- Custom thumbnails
- Exclusive commands
- priority support
"""
    await query.message.edit_caption(
        caption=text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="help_callback")]])
    )
