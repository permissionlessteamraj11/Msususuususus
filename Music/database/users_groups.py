from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI

mongodb = AsyncIOMotorClient(MONGO_DB_URI)
db = mongodb.PritiMusic

usersdb = db.users
groupsdb = db.groups

async def is_user_present(user_id: int):
    user = await usersdb.find_one({"user_id": user_id})
    return True if user else False

async def add_user(user_id: int):
    if not await is_user_present(user_id):
        return await usersdb.insert_one({"user_id": user_id})

async def is_group_present(chat_id: int):
    group = await groupsdb.find_one({"chat_id": chat_id})
    return True if group else False

async def add_group(chat_id: int):
    if not await is_group_present(chat_id):
        return await groupsdb.insert_one({"chat_id": chat_id})

async def get_served_users():
    users = usersdb.find({"user_id": {"$gt": 0}})
    return await users.to_list(length=1000000)

async def get_served_chats():
    chats = groupsdb.find({"chat_id": {"$lt": 0}})
    return await chats.to_list(length=1000000)
