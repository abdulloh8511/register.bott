from aiogram import types


phone_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text="📞 Telefon raqam", request_contact=True)]],
    resize_keyboard=True
)


tasdiqlash_kb = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="✅ Tasdiqlash")],
        [types.KeyboardButton(text="❌ Bekor qilish")]
    ],
    resize_keyboard=True
)
