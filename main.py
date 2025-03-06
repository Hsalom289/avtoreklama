from telethon import TelegramClient, errors
from telethon.tl.types import InputPeerChannel, InputPeerChat
import asyncio
import random
from datetime import datetime, timedelta
import sys

# Konfiguratsiya
API_ID = 21135417
API_HASH = '40963f632be1f4349a528780bf5393f2'
SESSION_NAME = 'userbot.session'
INTERVAL_HOURS = 1

# Xabarlar ro'yxati
MESSAGES = [
    "Assalomu alaykum guruxingizga 90/95% aktiv odam qoshib beraman✅ toza ayollar va aralash ishonchli odam qoshtirish uchun murojat qiling😍😍😍 Halollik foydadan ustun!!",
    # Boshqa xabarlar...
]

async def get_all_groups(client):
    """Barcha guruhlarni olish"""
    groups = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            try:
                chat = await client.get_entity(dialog.id)
                
                # 1.28.0 versiyasiga mos ruxsat tekshiruvi
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
                    print(f"✅ {dialog.name} qo'shildi")
                    
            except Exception as e:
                print(f"⚠️ {dialog.name} - Xato: {str(e)}")
    return groups

async def process_group(client, group):
    """Guruhda amallar bajaring"""
    try:
        # Xabar yuborish
        await client.send_message(group['entity'], random.choice(MESSAGES))
        print(f"✉️ {group['name']} ga xabar yuborildi")
        
        # Postlarni ko'rish (2-10 ta)
        post_count = random.randint(2, 3)
        posts = await client.get_messages(group['entity'], limit=post_count)
        for post in posts:
            if not post.out:
                print(f"👀 Post: {post.text[:50] if post.text else '[Media]'}")
                
        return True
        
    except errors.ChatWriteForbiddenError:
        print(f"❌ {group['name']} ga yozish taqiqlangan")
        return False
    except errors.FloodWaitError as e:
        print(f"⏳ Flood kutish: {e.seconds} soniya")
        await asyncio.sleep(e.seconds)
        return False
    except Exception as e:
        print(f"⚠️ {group['name']} - Xato: {str(e)}")
        return False

async def main_loop(client):
    """Asosiy tsikl"""
    while True:
        try:
            print(f"\n🔄 Yangi aylanish ({datetime.now().strftime('%H:%M')})")
            groups = await get_all_groups(client)
            random.shuffle(groups)
            
            for group in groups:
                if await process_group(client, group):
                    await asyncio.sleep(random.randint(10, 15))
                    
            print(f"⏳ Keyingi yuborish: {(datetime.now() + timedelta(hours=INTERVAL_HOURS)).strftime('%H:%M')}")
            await asyncio.sleep(INTERVAL_HOURS * 3600)
            
        except KeyboardInterrupt:
            print("\n⏹ Dastur to'xtatildi!")
            await client.disconnect()
            sys.exit()

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    try:
        await client.start()
        print("✅ Tizimga ulandi!")
        await main_loop(client)
    except Exception as e:
        print(f"⚠️ Xato: {str(e)}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())