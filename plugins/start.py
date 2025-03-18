from pyrogram import Client as MN_Bots
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait
import asyncio
import logging

# Logging setup
logging.getLogger().setLevel(logging.INFO)

@MN_Bots.on_message(filters.command("start"))
async def start(client: MN_Bots, msg: Message):
    try:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Me To Your Group", url=f"https://t.me/{client.me.username}?startgroup=true")],
            [InlineKeyboardButton("ℹ Help", callback_data="help_cb"),
             InlineKeyboardButton("📜 About", callback_data="about_cb")],
            [InlineKeyboardButton("💬 Support", url="https://t.me/mnbots_support"),
             InlineKeyboardButton("🌟 Source Code", url="https://github.com/mn-bots/auto-delete")]
        ])

        welcome_text = f"""
👋 **Hello, {msg.from_user.mention}!**  
I'm **{client.me.first_name}**, a powerful Telegram bot built to manage your groups effectively. 🚀  

🔹 **Features:**  
✅ Auto-delete messages  
✅ Admin-only commands  
✅ 24/7 uptime  
✅ Open source  

🔹 **Use the buttons below to explore more!**
"""

        await msg.reply_text(
            welcome_text,
            disable_web_page_preview=True,
            reply_markup=buttons,
        )

    except FloodWait as e:
        logging.warning(f"FloodWait detected! Sleeping for {e.value} seconds.")
        await asyncio.sleep(e.value)
        await start(client, msg)  # Retry after waiting

# Help Callback Handler
@MN_Bots.on_callback_query(filters.regex("help_cb"))
async def help_callback(client: MN_Bots, query: CallbackQuery):
    help_text = """
📌 **Help Section**  

➤ Use `/start` to restart the bot  
➤ Add me as **Admin** in your group  
➤ Messages will be **auto-deleted** within 3 minutes 

For more details, contact **Support** 👇  
"""
    await query.message.edit_text(
        help_text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start_cb")]])
    )

# About Callback Handler
@MN_Bots.on_callback_query(filters.regex("about_cb"))
async def about_callback(client: MN_Bots, query: CallbackQuery):
    about_text = f"""
🤖 **About This Bot**  

👤 **Developer:** [Your Name](https://t.me/mrmntg)  
⚡ **Version:** 1.0  
🛠 **Features:** Auto-delete, Admin commands, 24/7 Uptime  

🔹 **Want to add this bot to your group?** Click below!  
"""
    await query.message.edit_text(
        about_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Me", url=f"https://t.me/{client.me.username}?startgroup=true")],
            [InlineKeyboardButton("🔙 Back", callback_data="start_cb")]
        ])
    )

# Back to Start Callback Handler
@MN_Bots.on_callback_query(filters.regex("start_cb"))
async def back_to_start(client: MN_Bots, query: CallbackQuery):
    await start(client, query.message)  # Reuse the start function
