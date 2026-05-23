from pyrogram import filters
from pyrogram.types import CallbackQuery
from Music.core.call import call
from Music.helpers.queue import pop_from_queue, clear_queue
from Music.plugins.play import is_admin

@filters.on_callback_query(filters.regex("pause_cb"))
async def pause_cb(client, query: CallbackQuery):
    if not await is_admin(query.message.chat.id, query.from_user.id, client):
        return await query.answer("Admin only.", show_alert=True)

    await call.pause_stream_call(query.message.chat.id)
    await query.answer("Stream paused.")

@filters.on_callback_query(filters.regex("resume_cb"))
async def resume_cb(client, query: CallbackQuery):
    if not await is_admin(query.message.chat.id, query.from_user.id, client):
        return await query.answer("Admin only.", show_alert=True)

    await call.resume_stream_call(query.message.chat.id)
    await query.answer("Stream resumed.")

@filters.on_callback_query(filters.regex("skip_cb"))
async def skip_cb(client, query: CallbackQuery):
    if not await is_admin(query.message.chat.id, query.from_user.id, client):
        return await query.answer("Admin only.", show_alert=True)

    chat_id = query.message.chat.id
    next_song = await pop_from_queue(chat_id)
    if next_song:
        await call.join_call(chat_id, next_song["link"], video=next_song["video"])
        await query.message.edit_caption(f"⏭ Skipped.\n\n🎵 **Now Playing:** {next_song['title']}")
    else:
        await call.leave_call(chat_id)
        await query.message.edit_caption("⏭ Skipped. No more songs in queue.")
    await query.answer("Skipped.")

@filters.on_callback_query(filters.regex("stop_cb"))
async def stop_cb(client, query: CallbackQuery):
    if not await is_admin(query.message.chat.id, query.from_user.id, client):
        return await query.answer("Admin only.", show_alert=True)

    chat_id = query.message.chat.id
    await call.leave_call(chat_id)
    await clear_queue(chat_id)
    await query.message.edit_caption("⏹ Stream stopped and queue cleared.")
    await query.answer("Stopped.")
