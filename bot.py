import logging
import threading
from datetime import datetime, timedelta
from flask import Flask
from pyrogram import Client
from config import BOT, API, OWNER  # Removed CHANNEL

# Logging setup
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

# Flask app for health check
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8000)

class MN_Bot(Client):  

    def __init__(self):
        super().__init__(
            "MN-Bot",
            API.ID,
            API.HASH,
            bot_token=BOT.TOKEN,
            plugins=dict(root="plugins"),
            workers=16,
        )
        self.delete_before = 10  # Time range in minutes for message deletion

    async def start(self):
        await super().start()
        me = await self.get_me()
        if me.username:
            BOT.USERNAME = f"@{me.username}"
        self.mention = me.mention
        self.username = me.username

        await self.send_message(
            chat_id=int(OWNER.ID),
            text=f"{me.first_name} ✅✅ BOT started successfully ✅✅",
        )

        logging.info(f"{me.first_name} ✅✅ BOT started successfully ✅✅")

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Stopped 🙄")

    async def delete_old_messages(self, message):
        """ Delete messages in all groups where the bot is an admin """
        try:
            member = await self.get_chat_member(message.chat.id, "me")
            if member.status in ["administrator", "owner"]:  # Check if bot is an admin
                message_time = datetime.utcfromtimestamp(message.date)
                delete_before = datetime.utcnow() - timedelta(minutes=self.delete_before)

                if message_time >= delete_before:
                    await message.delete()
                    logging.info(f"Deleted message from {message.from_user.first_name} in {message.chat.title}")
        except Exception as e:
            logging.error(f"Failed to delete message in {message.chat.title}: {e}")

    async def on_message(self, message):
        """ Override the default message handler """
        await self.delete_old_messages(message)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    MN_Bot().run()
