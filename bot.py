import asyncio
from pyrogram import Client

# Railway mühit dəyişənlərindən məlumatları oxuyun
api_id = ""
api_hash = "BURA_API_HASH"
target_group = "qrup_username_veya_id"
message_text = "Salam, bu sizin üçün göndərilən avtomatik mesajdır."

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

