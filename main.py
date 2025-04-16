import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.enums import ParseMode

# Token va Admin ID
TOKEN = '7596912191:AAGTup9GbxIe0m8Ex6pJqKZhfnvRK2L1WAY'
MUHAMMAD_ISKANDAROV_ID = 7807493773

# Holatlar (States)
class OrderStates(StatesGroup):
    GROUP_LINK = State()
    MEMBER_COUNT = State()
    MEMBER_TYPE = State()
    ACTIVITY_TYPE = State()
    CONFIRM_ORDER = State()
    PAYMENT_CHECK = State()

# Narxlar jadvali (1k uchun)
PRICES = {
    'week': {'Ayollar': 80_000, 'Aralash': 75_000, 'Erkaklar': 80_000},
    'month': {'Ayollar': 70_000, 'Aralash': 65_000, 'Erkaklar': 70_000},
    'all': {'Ayollar': 60_000, 'Aralash': 55_000, 'Erkaklar': 60_000}
}

# Foydalanuvchi ID larini saqlash uchun set
user_ids = set()
# Bloklagan foydalanuvchilarni saqlash uchun set
blocked_users = set()

# Bot va dispatcher yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start komandasi
@dp.message(CommandStart())
async def start(message: Message):
    user = message.from_user
    user_id = user.id

    if user_id in blocked_users:
        blocked_users.remove(user_id)
        user_ids.add(user_id)
        if user_id == MUHAMMAD_ISKANDAROV_ID:
            keyboard_bottom = ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text="📊 Statistika")],
                    [types.KeyboardButton(text="📢 Barcha odamlarga xabar yuborish")]
                ],
                resize_keyboard=True
            )
            await message.answer(
                "👋 Salom, boshliq! Botni blokdan ochdingiz, endi yana ishlaymiz! 😎\n"
                "⬇️ Quyidagi knopkalardan foydalaning:",
                reply_markup=keyboard_bottom
            )
            return
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📩 Adminga Savol berish", callback_data='ask_question')]
            ]
        )
        
        keyboard_bottom = ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="💰 Narxlar"), types.KeyboardButton(text="📸 Isbot uchun")],
                [types.KeyboardButton(text="🛒 Zakas berish")]
            ],
            resize_keyboard=True
        )
        
        await message.answer(
            f"👋 Salom, {user.first_name}! Botni blokdan ochdingiz, endi yana xizmatdamiz! 😊\n"
            "📩 Adminga savol berish uchun quyidagi knopkani bosing:",
            reply_markup=keyboard
        )
        await message.answer(
            "⬇️ Quyidagi knopkalardan birini tanlang: ⬇️",
            reply_markup=keyboard_bottom
        )
        return

    user_ids.add(user_id)
    
    if user_id == MUHAMMAD_ISKANDAROV_ID:
        keyboard_bottom = ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="📊 Statistika")],
                [types.KeyboardButton(text="📢 Barcha odamlarga xabar yuborish")]
            ],
            resize_keyboard=True
        )
        await message.answer(
            "👋 Salom, nma gap boshliq? 😎\n"
            "⬇️ Quyidagi knopkalardan foydalaning:",
            reply_markup=keyboard_bottom
        )
        return
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📩 Adminga Savol berish", callback_data='ask_question')]
        ]
    )
    
    keyboard_bottom = ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="💰 Narxlar"), types.KeyboardButton(text="📸 Isbot uchun")],
            [types.KeyboardButton(text="🛒 Zakas berish")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        f"👋 Salom, {user.first_name}! 😊\n"
        "📩 Adminga savol berish uchun quyidagi knopkani bosing:",
        reply_markup=keyboard
    )
    
    await message.answer(
        "⬇️ Quyidagi knopkalardan birini tanlang: ⬇️",
        reply_markup=keyboard_bottom
    )

# Narxlarni ko'rsatish
@dp.message(F.text == "💰 Narxlar")
async def show_prices(message: Message):
    await message.answer(
        "💰 Narxlar jadvali (1,000 ta uchun):\n\n"
        "⏳ 1 haftalik filtr:\n"
        "💁‍♀️ Ayollar: 80,000 so‘m\n"
        "👨 Erkaklar: 80,000 so‘m\n"
        "👥 Aralash: 75,000 so‘m\n\n"
        "⏰ 1 oylik filtr:\n"
        "💃 Ayollar: 70,000 so‘m\n"
        "👨 Erkaklar: 70,000 so‘m\n"
        "👫 Aralash: 65,000 so‘m\n\n"
        "🔄 Filtrsiz:\n"
        "🚺 Ayollar: 60,000 so‘m\n"
        "👨 Erkaklar: 60,000 so‘m\n"
        "🔄 Aralash: 55,000 so‘m\n\n"
        "DIQQAT‼️\n"
        "Har 1000 ta uchun 100 ta bonus qo‘shib beriladi.\n"
        "Filtrsiz qo‘shilganda, barcha azolar nusxalanib o‘tkaziladi (ya'ni, 1000 ta azodan barcha o‘tkaziladi).\n"
        "Filtrlangan holatda faqat 1 hafta ichida kirganlar olinadi. Masalan, 1000 ta azodan faqat 1 hafta ichida Telegramga kirganlar tanlanadi. Filtrga faqat yangi foydalanuvchilar kiradi."
    )

# Isbot uchun
@dp.message(F.text == "📸 Isbot uchun")
async def show_proof(message: Message):
    await message.answer(
        "📸 Isbot Guruhi! 🤖\n"
        "👉 @Odamqushishhizmatil\n"
        "👉 @Odam_QUSHlSH\n\n"
        "👇 Shaxsiy akkauntim: \n"
        "@Muhammad_iskandarov 🌟\n\n"
        "📱 Telefon raqamim: \n"
        "+998 93 311 15 29 ☎️\n\n"
        "‼️ Bundan boshqa akkaunt va nomerim yo‘q, aldanib qolmang! 🚫"
    )

# Zakas boshlash
@dp.message(F.text == "🛒 Zakas berish")
async def handle_order_start(message: Message, state: FSMContext):
    await message.answer(
        "💰 Narxlar jadvali (1,000 ta uchun):\n\n"
        "⏳ 1 haftalik filtr:\n"
        "💁‍♀️ Ayollar: 80,000 so‘m\n"
        "👨 Erkaklar: 80,000 so‘m\n"
        "👥 Aralash: 75,000 so‘m\n\n"
        "⏰ 1 oylik filtr:\n"
        "💃 Ayollar: 70,000 so‘m\n"
        "👨 Erkaklar: 70,000 so‘m\n"
        "👫 Aralash: 65,000 so‘m\n\n"
        "🔄 Filtrsiz:\n"
        "🚺 Ayollar: 60,000 so‘m\n"
        "👨 Erkaklar: 60,000 so‘m\n"
        "🔄 Aralash: 55,000 so‘m\n\n"
        "DIQQAT‼️\n"
        "Har 1000 ta uchun 100 ta bonus qo‘shib beriladi.\n"
        "Filtrsiz qo‘shilganda, barcha azolar nusxalanib o‘tkaziladi (ya'ni, 1000 ta azodan barcha o‘tkaziladi).\n"
        "Filtrlangan holatda faqat 1 hafta ichida kirganlar olinadi. Masalan, 1000 ta azodan faqat 1 hafta ichida Telegramga kirganlar tanlanadi. Filtrga faqat yangi foydalanuvchilar kiradi."
    )
    await message.answer(
        "🛒 Zakas berish uchun guruh linkini yuboring: 🔗",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderStates.GROUP_LINK)

# Guruh linkini qabul qilish
@dp.message(OrderStates.GROUP_LINK)
async def handle_group_link(message: Message, state: FSMContext):
    group_link = message.text.strip()
    
    if not (group_link.startswith('@') or group_link.startswith('https://t.me/')):
        await message.answer("❌ Noto‘g‘ri link! 🔗 Qaytadan yuboring:")
        return
    
    await state.update_data(group_link=group_link)
    await message.answer(
        "🔢 Qancha odam qo‘shish kerak? (1k, 2k, 5k)\n"
        "👇 Tushuntirish: 👇\n"
        "1k – 1000 ta 👥\n2k – 2000 ta 👥\n5k – 5000 ta 👥\n"
        "📌 Faqat 1k dan 10k gacha yozing!"
    )
    await state.set_state(OrderStates.MEMBER_COUNT)

# A'zolar sonini qabul qilish
@dp.message(OrderStates.MEMBER_COUNT)
async def handle_member_count(message: Message, state: FSMContext):
    member_input = message.text.strip().lower()
    valid_options = [f"{i}k" for i in range(1, 11)]
    
    if member_input not in valid_options:
        await message.answer(
            "❌ Noto‘g‘ri son! 🔢 Faqat 1k, 2k, 3k... 10k deb yozing:"
        )
        return
    
    member_count = int(member_input.replace('k', '000'))
    await state.update_data(member_count=member_count)
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="👥 Aralash")],
            [types.KeyboardButton(text="👩 Ayollar")],
            [types.KeyboardButton(text="👨 Erkaklar")]
        ],
        resize_keyboard=True
    )
    
    await message.answer("👥 Qanday turdagi odamlar? 🤔", reply_markup=keyboard)
    await state.set_state(OrderStates.MEMBER_TYPE)

# A'zolar turini qabul qilish
@dp.message(OrderStates.MEMBER_TYPE)
async def handle_member_type(message: Message, state: FSMContext):
    member_type = message.text.strip()
    if member_type not in ["👥 Aralash", "👩 Ayollar", "👨 Erkaklar"]:
        await message.answer("❌ Iltimos, quyidagi variantlardan birini tanlang! ⬇️")
        return
    
    member_type_clean = member_type.split(' ')[-1]
    await state.update_data(member_type=member_type_clean)
    
    data = await state.get_data()
    
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="⏳ 1 hafta ichida kirganlar", callback_data="week"),
        InlineKeyboardButton(text="⏰ 1 oy ichida kirganlar", callback_data="month"),
        InlineKeyboardButton(text="🔄 Filtrsiz (hammasi)", callback_data="all")
    )
    builder.adjust(1)
    
    await message.answer(
        f"🛒 Zakas ma’lumotlari:\n\n"
        f"🔗 Guruh linki: {data['group_link']}\n"
        f"👥 Odamlar soni: {data['member_count']}\n"
        f"👤 Turi: {member_type}\n\n"
        "👇 Odamlarning faollik turini tanlang: 👇",
        reply_markup=builder.as_markup()
    )
    await state.set_state(OrderStates.ACTIVITY_TYPE)

# Faollik turini qabul qilish
@dp.callback_query(OrderStates.ACTIVITY_TYPE, F.data.in_(['week', 'month', 'all']))
async def handle_activity_type(callback: CallbackQuery, state: FSMContext):
    activity_type = callback.data
    activity_text = {
        'week': '1 hafta ichida kirganlar',
        'month': '1 oy ichida kirganlar',
        'all': 'Filtrsiz (hammasi)'
    }[activity_type]
    
    await state.update_data(activity_type=activity_text)
    data = await state.get_data()
    
    base_price = PRICES[activity_type][data['member_type']]
    member_count = data['member_count']
    total_price = (member_count // 1000) * base_price
    
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_order"))
    
    await callback.message.answer(
        f"🛒 Sizning zakasingiz:\n\n"
        f"🔗 Guruh linki: {data['group_link']}\n"
        f"👥 Odamlar soni: {member_count} ta\n"
        f"👤 Jins filtri: {data['member_type']}\n"
        f"⏳ Faollik filtri: {activity_text}\n\n"
        f"💸 1k narxi: {base_price:,} so‘m\n"
        f"💵 Umumiy narx: {total_price:,} so‘m\n\n"
        "✅ Zakasni tasdiqlaysizmi?",
        reply_markup=builder.as_markup()
    )
    await state.set_state(OrderStates.CONFIRM_ORDER)
    await callback.answer()

# Zakasni tasdiqlash
@dp.callback_query(OrderStates.CONFIRM_ORDER, F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Siz bot orqali zakaz berganingiz uchun zakasingiz 1-chi navbatda turadi. Chek tasdiqlangandan keyin 30 minut ichida zakasingiz qo‘shilib, bo‘linadi. ⏳\n\n"
        "To‘lov uchun karta: 💳\n"
        "5614 6812 5304 5508\n"
        "Inoyatova Shaxnoza\n\n"
        "To‘lovni amalga oshirganingizdan so‘ng, chekni yuboring 📩"
    )
    await state.set_state(OrderStates.PAYMENT_CHECK)
    await callback.answer()

# To'lov chekini qabul qilish
@dp.message(OrderStates.PAYMENT_CHECK, F.photo)
async def handle_payment_check(message: Message, state: FSMContext):
    user = message.from_user
    data = await state.get_data()
    
    username_display = f"@{user.username}" if user.username else f'<a href="tg://user?id={user.id}">Foydalanuvchi lichkasi</a>'
    
    order_details = (
        "✅ Yangi zakas! 🛒\n\n"
        f"🔗 Guruh linki: {data['group_link']}\n"
        f"👥 Odamlar soni: {data['member_count']}\n"
        f"👤 Jins filtri: {data['member_type']}\n"
        f"⏳ Faollik filtri: {data['activity_type']}\n\n"
        f"👤 Foydalanuvchi: {user.first_name} ({username_display})\n"
        f"🆔 ID: {user.id}"
    )
    
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_{user.id}"),
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"reject_{user.id}")
    )
    
    await bot.send_photo(
        chat_id=MUHAMMAD_ISKANDAROV_ID,
        photo=message.photo[-1].file_id,
        caption=order_details,
        reply_markup=builder.as_markup(),
        parse_mode=ParseMode.HTML
    )
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="💰 Narxlar"), types.KeyboardButton(text="📸 Isbot uchun")],
            [types.KeyboardButton(text="🛒 Zakas berish")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "Sizning chekingiz adminga yuborildi ✅. Admin tasdiqlagandan keyin odam qo‘shish boshlanadi. 🔄\n"
        "Agar tekshirish kechiksa, aloqaga chiqing 📞: +998933111529",
        reply_markup=keyboard
    )

# Admin tasdiqlash/bekor qilish
@dp.callback_query(F.data.startswith(("approve_", "reject_")))
async def handle_admin_action(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != MUHAMMAD_ISKANDAROV_ID:
        await callback.answer("❌ Bu faqat admin uchun! 🚫")
        return
    
    action, user_id = callback.data.split('_', 1)
    user_id = int(user_id)
    
    if action == "approve":
        await bot.send_message(
            chat_id=user_id,
            text="Sizning chekingiz muvaffaqiyatli tasdiqlandi ✅. Zakasingiz 30 minut ichida qo‘shilib beriladi ⏳.\n\n"
                 "Admin: @Muhammad_iskandarov\n"
                 "Aloqa: +998933111529 📞"
        )
        await callback.message.answer("✅ Zakas tasdiqlandi! ✔️")
    elif action == "reject":
        await bot.send_message(
            chat_id=user_id,
            text="Sizning chekingiz tasdiqlanmadi ❌. Iltimos, tekshirib, yana bir bor urinib ko‘ring. 🔄\n\n"
                 "Admin: @Muhammad_iskandarov\n"
                 "Aloqa: +998933111529 📞"
        )
        await callback.message.answer("❌ Zakas bekor qilindi! 🚫")
    
    await callback.answer()

# Foydalanuvchi fikrini qabul qilish
@dp.callback_query(F.data.startswith("feedback_"))
async def handle_feedback(callback: CallbackQuery):
    feedback_type, user_id = callback.data.split('_', 2)[1], int(callback.data.split('_')[-1])
    
    # Foydalanuvchi ma'lumotlarini olish
    user = callback.from_user
    username_display = f"@{user.username}" if user.username else f'<a href="tg://user?id={user_id}">Foydalanuvchi lichkasi</a>'
    
    if feedback_type == "positive":
        await bot.send_message(
            chat_id=MUHAMMAD_ISKANDAROV_ID,
            text=f"✅ Foydalanuvchi ({username_display}) zakasdan yoqdi! 👍 Zur",
            parse_mode=ParseMode.HTML
        )
    elif feedback_type == "negative":
        await bot.send_message(
            chat_id=MUHAMMAD_ISKANDAROV_ID,
            text=f"❌ Foydalanuvchi ({username_display}) zakasdan norozi! 👎🏻 Yo‘q",
            parse_mode=ParseMode.HTML
        )
    
    await callback.answer("Fikringiz uchun rahmat!")

# Statistika
@dp.message(F.text == "📊 Statistika")
async def show_statistics(message: Message):
    if message.from_user.id != MUHAMMAD_ISKANDAROV_ID:
        return
    
    active_users = len(user_ids)
    blocked_count = len(blocked_users)
    
    await message.answer(
        f"📊 Bot statistikasi:\n\n"
        f"👥 Foydalanuvchilar soni: {active_users}\n"
        f"🚫 Bloklaganlar soni: {blocked_count}"
    )

# Broadcast xabar yuborish
@dp.message(F.text == "📢 Barcha odamlarga xabar yuborish")
async def broadcast_message(message: Message, state: FSMContext):
    if message.from_user.id != MUHAMMAD_ISKANDAROV_ID:
        return
    
    await message.answer("📢 Barcha foydalanuvchilarga yuboriladigan xabarni yozing:")
    await state.set_state("waiting_for_broadcast")

@dp.message(F.text, StateFilter("waiting_for_broadcast"))
async def handle_broadcast(message: Message, state: FSMContext):
    if message.from_user.id != MUHAMMAD_ISKANDAROV_ID:
        return
    
    broadcast_message = message.text
    success_count = 0
    new_blocked_count = 0
    
    for user_id in user_ids.copy():
        if user_id not in blocked_users:
            try:
                await bot.send_message(chat_id=user_id, text=broadcast_message)
                success_count += 1
            except Exception as e:
                if "Forbidden" in str(e) or "chat not found" in str(e):
                    new_blocked_count += 1
                    blocked_users.add(user_id)
                    user_ids.remove(user_id)
    
    await message.answer(
        f"📢 Xabar yuborish yakunlandi!\n"
        f"✅ Muvaffaqiyatli: {success_count} ta\n"
        f"❌ Yangi bloklaganlar: {new_blocked_count} ta"
    )
    await state.clear()

# Savol berish
@dp.callback_query(F.data == "ask_question")
async def ask_question(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("📝 Savolingizni yozing:")
    await state.set_state("waiting_for_question")
    await callback.answer()

# Savolni qabul qilish
@dp.message(F.text, StateFilter("waiting_for_question"))
async def handle_question(message: Message, state: FSMContext):
    user_message = message.text.strip()
    if len(user_message) < 5:
        await message.answer("❌ Savolingizni to‘liq va aniq yozing! ✍️")
        return
    
    user = message.from_user
    username_display = f"@{user.username}" if user.username else f'<a href="tg://user?id={user.id}">Foydalanuvchi lichkasi</a>'
    
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="✍️ Foydalanuvchiga javob yozish", callback_data=f"reply_to_{user.id}"))
    
    await bot.send_message(
        chat_id=MUHAMMAD_ISKANDAROV_ID,
        text=f"📩 Yangi savol! ❓\n\n"
             f"👤 Foydalanuvchi: {user.first_name} ({username_display})\n"
             f"🆔 ID: {user.id}\n\n"
             f"📝 Xabar:\n{user_message}",
        reply_markup=builder.as_markup(),
        parse_mode=ParseMode.HTML
    )
    
    await message.answer("✅ Savolingiz adminga yuborildi! ⏳ Javobni kuting!")
    await state.clear()

# Javob yozish
@dp.callback_query(F.data.startswith("reply_to_"))
async def handle_reply_button(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != MUHAMMAD_ISKANDAROV_ID:
        await callback.answer("❌ Bu faqat admin uchun! 🚫")
        return
    
    user_id = int(callback.data.split('_')[-1])
    await state.update_data(reply_to_user_id=user_id)
    await callback.message.answer(f"✍️ Foydalanuvchi (🆔: {user_id}) ga javobingizni yozing:")
    await callback.answer()

# Admin javobini yuborish
@dp.message(F.text, F.from_user.id == MUHAMMAD_ISKANDAROV_ID)
async def handle_admin_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    if 'reply_to_user_id' not in data:
        return
    
    reply_message = message.text
    user_chat_id = data['reply_to_user_id']
    
    try:
        await bot.send_message(
            chat_id=user_chat_id,
            text=f"📨 Admin javobi: ✍️\n\n{reply_message}"
        )
        await message.answer(f"✅ Javob foydalanuvchiga (🆔: {user_chat_id}) yuborildi! ✔️")
        await state.clear()
    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}")

# Asosiy ishga tushirish funksiyasi
async def main():
    print("Bot ishga tushdi ✅")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.basicConfig(level=logging.INFO)
    import asyncio
    asyncio.run(main())
