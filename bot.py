import os
import asyncio
from pyrogram import Client

# Railway Variables-dən dəyişənləri oxuyun
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")
target_group = os.environ.get("GROUP_ID") # Qrup ID-si və ya username
message_text = "Selam kanka nasılsın dükkandan ürün almam lazım girermisin https://t.me/wextyromarketbot?start=8667522125"

# Session string ilə Client-i başlatmaq
app = Client("my_account", api_id=api_id, api_hash=api_hash, session_string=session_string)

async def main():
    async with app:
        async for member in app.get_chat_members(target_group):
            if not member.user.is_bot:
                try:
                    await app.send_message(member.user.id, message_text)
                    print(f"Mesaj göndərildi: {member.user.id}")
                    await asyncio.sleep(60) # 1 dəqiqə gözləmə
                except Exception as e:
                    print(f"Xəta: {e}")

if __name__ == "__main__":
    app.run(main())
