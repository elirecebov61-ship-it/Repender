import asyncio
import os
import sys
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.sessions import StringSession
import logging

# ===== LOGGING =====
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# ===== ENV DƏYIŞKƏNLƏRI =====
API_ID = int(os.getenv("TELEGRAM_API_ID", "0"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "")

# String session (Railway-də)
SESSION_STRING = os.getenv("SESSION_STRING_1", None)

# Qrupların chat ID-ləri
TARGET_GROUPS_STR = os.getenv("TARGET_GROUPS", "-1003987036631,-1001262463392")
TARGET_GROUPS = [int(gid.strip()) for gid in TARGET_GROUPS_STR.split(",")]

# Mesaj
MESSAGE = os.getenv(
    "ADVERTISE_MESSAGE",
    "Selam! Marketten Ürün Almak için Puana İhtiyacım var Lütfen Girermisin https://t.me/wextyromarketbot?start=8034872992"
)

# Gecikme (saniyə)
DELAY_BETWEEN_MESSAGES = int(os.getenv("DELAY_BETWEEN_MESSAGES", "2"))

# ===== SESSION STRING YARAT =====
async def create_session():
    """İlk login: session string yarat"""
    if API_ID == 0 or API_HASH == "":
        print("❌ TELEGRAM_API_ID və TELEGRAM_API_HASH boşdur!")
        return
    
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.start()
    
    session_string = client.session.save()
    print(f"\n✅ SESSION_STRING (bunu .env-ə əlavə et):\n")
    print(session_string)
    print("\n☝️ Əlavə et: SESSION_STRING_1={session_string}")
    
    await client.disconnect()

# ===== STRING SESSION İLƏ MESAJ GÖN =====
async def send_messages_string():
    """Railway-də string session ilə mesaj gönder"""
    if not SESSION_STRING:
        logger.error("❌ SESSION_STRING tapılmadı!")
        logger.error("Lokal: python userbot.py --create-session")
        logger.error("Railway: Environment variables-ə əlavə et")
        return
    
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    
    try:
        await client.connect()
        logger.info("✅ Bağlandı")
        
        for group_id in TARGET_GROUPS:
            try:
                await client.send_message(group_id, MESSAGE)
                logger.info(f"✅ {group_id}: Mesaj göndərildi")
                await asyncio.sleep(DELAY_BETWEEN_MESSAGES)
            except FloodWaitError as e:
                logger.warning(f"⚠️ Flood: {e.seconds}s gözləyirəm...")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                logger.error(f"❌ {group_id}: {e}")
        
        await client.disconnect()
        logger.info("✅ Bütün mesajlar göndərildi!")
    except Exception as e:
        logger.error(f"❌ Xəta: {e}")

# ===== LOCAL SESSION FAYLLARINDAN =====
async def send_messages_local():
    """Lokal session fayllarından (session1, session2, session3)"""
    sessions = ["session1", "session2", "session3"]
    
    async def send_single(session_name):
        client = TelegramClient(session_name, API_ID, API_HASH)
        try:
            await client.start()
            logger.info(f"✅ {session_name} bağlandı")
            
            for group_id in TARGET_GROUPS:
                try:
                    await client.send_message(group_id, MESSAGE)
                    logger.info(f"✅ {session_name} → {group_id}")
                    await asyncio.sleep(DELAY_BETWEEN_MESSAGES)
                except FloodWaitError as e:
                    logger.warning(f"⚠️ Flood: {e.seconds}s")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    logger.error(f"❌ {session_name} → {group_id}: {e}")
            
            await client.disconnect()
        except Exception as e:
            logger.error(f"❌ {session_name}: {e}")
    
    tasks = [send_single(s) for s in sessions]
    await asyncio.gather(*tasks)

# ===== MAIN =====
async def main():
    logger.info("🚀 Userbot başladı...\n")
    
    if SESSION_STRING:
        logger.info("📡 String session (Railway)")
        await send_messages_string()
    else:
        logger.info("💾 Local sessions (Lokal)")
        await send_messages_local()

if __name__ == "__main__":
    if "--create-session" in sys.argv:
        logger.info("🔑 Session yaradılıyor...")
        asyncio.run(create_session())
    else:
        asyncio.run(main())
