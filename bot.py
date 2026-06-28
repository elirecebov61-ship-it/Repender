import asyncio
from pyrogram import Client

# Railway mühit dəyişənlərindən məlumatları oxuyun
api_id = "39359457"
api_hash = "c310059258a8b03d394e94b615805d13"
target_group = "israiltehdit"
message_text = "Selam kanka nasılsın dükkandan ürün almam lazım girermisin https://t.me/wextyromarketbot?start=8667522125"

app = Client("my_account", api_id=api_id, api_hash=api_hash)

async def main():
    async with app:
        # Qrupdakı üzvləri çəkirik
        async for member in app.get_chat_members(target_group):
            if not member.user.is_bot:
                try:
                    print(f"Mesaj göndərilir: {member.user.first_name}")
                    await app.send_message(member.user.id, message_text)
                    # 1 dəqiqəlik interval
                    await asyncio.sleep(60)
                except Exception as e:
                    print(f"Xəta baş verdi: {e}")

if __name__ == "__main__":
    app.run(main())

