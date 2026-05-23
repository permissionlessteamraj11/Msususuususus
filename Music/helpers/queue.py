from Music.database.users_groups import db

queuedb = db.queue

async def add_to_queue(chat_id, title, link, duration, user_id, thumb, video=False):
    count = await queuedb.count_documents({"chat_id": chat_id})
    await queuedb.insert_one({
        "chat_id": chat_id,
        "title": title,
        "link": link,
        "duration": duration,
        "user_id": user_id,
        "thumb": thumb,
        "video": video,
        "position": count + 1
    })
    return count + 1

async def get_queue(chat_id):
    cursor = queuedb.find({"chat_id": chat_id}).sort("position", 1)
    return await cursor.to_list(length=100)

async def pop_from_queue(chat_id):
    next_song = await queuedb.find_one_and_delete({"chat_id": chat_id, "position": 1})
    if next_song:
        await queuedb.update_many(
            {"chat_id": chat_id},
            {"$inc": {"position": -1}}
        )
    return next_song

async def clear_queue(chat_id):
    await queuedb.delete_many({"chat_id": chat_id})
