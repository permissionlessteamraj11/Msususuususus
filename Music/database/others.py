from Music.database.users_groups import db

premiumdb = db.premium
blacklistdb = db.blacklist
settingsdb = db.settings

# Premium
async def is_premium_user(user_id: int):
    user = await premiumdb.find_one({"user_id": user_id})
    return True if user else False

async def add_premium_user(user_id: int):
    if not await is_premium_user(user_id):
        return await premiumdb.insert_one({"user_id": user_id})

async def remove_premium_user(user_id: int):
    return await premiumdb.delete_one({"user_id": user_id})

# Blacklist
async def is_blacklisted_user(user_id: int):
    user = await blacklistdb.find_one({"user_id": user_id})
    return True if user else False

async def blacklist_user(user_id: int):
    if not await is_blacklisted_user(user_id):
        return await blacklistdb.insert_one({"user_id": user_id})

async def whitelist_user(user_id: int):
    return await blacklistdb.delete_one({"user_id": user_id})

# Chat Settings
async def get_settings(chat_id: int):
    settings = await settingsdb.find_one({"chat_id": chat_id})
    if not settings:
        return {
            "chat_id": chat_id,
            "play_type": "everyone", # everyone/admin
            "quality": "high",
            "volume": 100,
        }
    return settings

async def update_settings(chat_id: int, key: str, value: str):
    await settingsdb.update_one(
        {"chat_id": chat_id},
        {"$set": {key: value}},
        upsert=True
    )
