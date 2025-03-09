from telethon import TelegramClient, errors
from telethon.tl.types import InputPeerChannel
import asyncio
import random
from datetime import datetime, timedelta
import sys
import logging

# Loglarni sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Konfiguratsiya
API_ID = 21135417  # O'z API_ID ni kiriting
API_HASH = '40963f632be1f4349a528780bf5393f2'  # O'z API_HASH ni kiriting
SESSION_NAME = 'userbot.session'  # Session fayli nomi
INTERVAL_HOURS = 1  # Xabarlarni tarqatish oralig'i (soatda)

# Xabarlar ro'yxati
MESSAGES = [
    "Assalomu alaykum guruxingizga 90/95% aktiv odam qoshib beraman✅ toza ayollar va aralash ishonchli odam qoshtirish uchun murojat qiling😍😍😍 Halollik foydadan ustun!!",
    # Boshqa xabarlar...
]

# Guruhlar ro'yxati
groups = []
processed_groups = set()  # Tarqatib bo'lingan guruhlar
failed_groups = set()     # Tarqatib bo'lmagan guruhlar

# Statistika
stats = {
    "messages_sent": 0,
    "errors": 0,
    "new_groups": 0,
    "retry_groups": 0
}

async def get_all_groups(client):
    """Barcha guruhlarni olish"""
    global groups
    groups = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            try:
                chat = await client.get_entity(dialog.id)
                
                # Ruxsatlarni tekshirish
                if isinstance(chat, InputPeerChannel):
                    can_send = chat.broadcast or (chat.megagroup and not chat.restricted)
                else:
                    can_send = not chat.restricted
                
                if can_send:
                    groups.append({
                        'id': dialog.id,
                        'name': dialog.name,
                        'entity': chat
                    })
                    logger.info(f"✅ {dialog.name} qo'shildi")
                    
            except Exception as e:
                logger.error(f"⚠️ {dialog.name} - Xato: {str(e)}", exc_info=True)
    return groups

async def handle_spam_block(client):
    """Spam blokini hal qilish"""
    logger.info("🛑 Spam blokini bartaraf qilish...")
    try:
        spam_bot = await client.get_entity("SpamBot")
        
        # 1-chi /start
        await client.send_message(spam_bot, "/start")
        await asyncio.sleep(5)
        
        # 2-chi /start
        await client.send_message(spam_bot, "/start")
        await asyncio.sleep(5)
        
        # Javobni tekshirish
        messages = await client.get_messages(spam_bot, limit=1)
        if messages and "CAPTCHA" in messages[0].text:
            logger.warning("⚠️ Iltimos CAPTCHA ni qo'lda hal qiling!")
            return False
        return True
        
    except Exception as e:
        logger.error(f"SpamBot xatosi: {str(e)}", exc_info=True)
        return False

async def send_message(client, group):
    """Xabar yuborish"""
    try:
        if group['id'] in failed_groups:
            logger.info(f"⏩ {group['name']} guruhiga avval tarqatib bo'lmagan, o'tkazib yuborildi")
            return False
            
        message = random.choice(MESSAGES)
        await client.send_message(group['entity'], message)
        logger.info(f"✉️ {group['name']} ga xabar yuborildi")
        processed_groups.add(group['id'])  # Tarqatib bo'lingan guruhga qo'shish
        stats["messages_sent"] += 1
        return True
    except errors.ChatWriteForbiddenError:
        logger.warning(f"❌ {group['name']} ga yozish taqiqlangan")
        failed_groups.add(group['id'])
        stats["errors"] += 1
        return False
    except errors.FloodWaitError as e:
        logger.warning(f"⏳ Flood kutish: {e.seconds} soniya")
        await asyncio.sleep(e.seconds)
        return False
    except errors.RPCError as e:
        if "SPAM" in str(e):
            logger.warning("🛑 Spam bloki aniqlandi, SpamBot ga murojaat qilinmoqda...")
            if await handle_spam_block(client):
                return await send_message(client, group)
        logger.error(f"⚠️ {group['name']} - Xato: {str(e)}", exc_info=True)
        stats["errors"] += 1
        return False
    except errors.ConnectionError as e:
        logger.error(f"⚠️ Ulanish xatosi: {str(e)}", exc_info=True)
        await asyncio.sleep(60)  # 1 daqiqa kutish va qayta urinish
        return False

async def distribute_messages(client):
    """Xabarlarni tarqatish"""
    global groups
    while True:
        try:
            if not client.is_connected():
                logger.warning("Ulanish uzilgan, qayta ulanmoqda...")
                await client.connect()
            
            logger.info(f"\n🔄 Yangi aylanish ({datetime.now().strftime('%H:%M')})")
            
            # Guruhlarni yangilash
            groups = await get_all_groups(client)
            if not groups:
                logger.warning("❌ Hech qanday guruh topilmadi!")
                await asyncio.sleep(600)
                continue
                
            random.shuffle(groups)
            
            for group in groups:
                if group['id'] not in processed_groups:
                    stats["new_groups"] += 1
                else:
                    stats["retry_groups"] += 1
                    
                if await send_message(client, group):
                    await asyncio.sleep(random.randint(10, 15))
                
            # Statistika
            logger.info(f"📊 Statistika: "
                       f"Yuborilgan xabarlar: {stats['messages_sent']}, "
                       f"Xatolar: {stats['errors']}, "
                       f"Yangi guruhlar: {stats['new_groups']}, "
                       f"Qayta urinishlar: {stats['retry_groups']}")
            
            # Statistikani yangilash
            stats["new_groups"] = 0
            stats["retry_groups"] = 0
            
            # Dam olish
            logger.info(f"⏳ Keyingi yuborish: {(datetime.now() + timedelta(hours=INTERVAL_HOURS)).strftime('%H:%M')}")
            await asyncio.sleep(INTERVAL_HOURS * 3600)
            
        except KeyboardInterrupt:
            logger.info("\n⏹ Dastur to'xtatildi!")
            await client.disconnect()
            sys.exit()
        except Exception as e:
            logger.error(f"🔥 Xato: {str(e)}", exc_info=True)
            await asyncio.sleep(300)

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    try:
        await client.start()
        logger.info("✅ Tizimga ulandi!")
        await distribute_messages(client)
    except errors.ConnectionError as e:
        logger.error(f"⚠️ Ulanish xatosi: {str(e)}", exc_info=True)
        await asyncio.sleep(60)  # 1 daqiqa kutish va qayta urinish
    except Exception as e:
        logger.error(f"⚠️ Kirish xatosi: {str(e)}", exc_info=True)
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
