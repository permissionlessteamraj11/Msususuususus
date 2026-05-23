import asyncio
from pyrogram import filters
from pyrogram.types import Message
import config
from Music.database.users_groups import get_served_users, get_served_chats
from Music.database.others import blacklist_user, whitelist_user, add_premium_user, remove_premium_user

@filters.on_message(filters.command("stats") & filters.user(config.OWNER_ID))
async def stats_command(client, message: Message):
    users = await get_served_users()
    chats = await get_served_chats()
    await message.reply_text(f"📊 **PritiMusic Stats:**\n\n👤 **Users:** {len(users)}\n💬 **Chats:** {len(chats)}")

@filters.on_message(filters.command("broadcast") & filters.user(config.OWNER_ID))
async def broadcast_command(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to broadcast it.")

    m = await message.reply_text("Broadcasting...")
    users = await get_served_users()
    count = 0
    for user in users:
        try:
            await message.reply_to_message.forward(user["user_id"])
            count += 1
            await asyncio.sleep(0.3) # Increased sleep for flood avoidance
        except Exception:
            pass
    await m.edit(f"✅ Broadcasted to {count} users.")

async def get_id(message: Message):
    if len(message.command) < 2:
        return None
    try:
        return int(message.command[1])
    except ValueError:
        return None

@filters.on_message(filters.command("addpremium") & filters.user(config.OWNER_ID))
async def add_premium(client, message: Message):
    user_id = await get_id(message)
    if not user_id:
        return await message.reply_text("Usage: /addpremium [user_id]")
    await add_premium_user(user_id)
    await message.reply_text(f"✅ User {user_id} added to premium.")

@filters.on_message(filters.command("rmpremium") & filters.user(config.OWNER_ID))
async def rm_premium(client, message: Message):
    user_id = await get_id(message)
    if not user_id:
        return await message.reply_text("Usage: /rmpremium [user_id]")
    await remove_premium_user(user_id)
    await message.reply_text(f"✅ User {user_id} removed from premium.")

@filters.on_message(filters.command("blacklist") & filters.user(config.OWNER_ID))
async def blacklist_command(client, message: Message):
    user_id = await get_id(message)
    if not user_id:
        return await message.reply_text("Usage: /blacklist [user_id]")
    await blacklist_user(user_id)
    await message.reply_text(f"✅ User {user_id} blacklisted.")

@filters.on_message(filters.command("whitelist") & filters.user(config.OWNER_ID))
async def whitelist_command(client, message: Message):
    user_id = await get_id(message)
    if not user_id:
        return await message.reply_text("Usage: /whitelist [user_id]")
    await whitelist_user(user_id)
    await message.reply_text(f"✅ User {user_id} whitelisted.")
