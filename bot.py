import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from db import jadval_yaratish, add_user
from keyboards import phone_keyboard, tasdiqlash_kb
from config import API_TOKEN, ADMIN_ID
from states import RegisterState

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(msg: types.Message):
    await msg.answer("Xush kelibsiz, Registratsiya uchun /register bosing")

@dp.message(Command("register"))
async def register_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Ismingizni kiriting")
    await state.set_state(RegisterState.name)

@dp.message(StateFilter(RegisterState.name))
async def name_handler(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Familiangizni kiriting")
    await state.set_state(RegisterState.surname)

@dp.message(StateFilter(RegisterState.surname))
async def surname_handler(msg: types.Message, state: FSMContext):
    await state.update_data(surname=msg.text)
    await msg.answer("Yoshingizni kiriting")
    await state.set_state(RegisterState.age)


@dp.message(StateFilter(RegisterState.age))
async def age_handler(msg: types.Message, state: FSMContext):
    await state.update_data(age=msg.text)
    await msg.answer("Telefon raqamingizni yuboring", reply_markup=phone_keyboard)
    await state.set_state(RegisterState.phone)


@dp.message(StateFilter(RegisterState.phone))
async def phone_handler(msg: types.Message, state: FSMContext):
    if msg.contact:
        phone = msg.contact.phone_number
    else:
        await msg.answer("Faqat telefon tugmasini bosish kerak", reply_markup=phone_keyboard)
        await state.set_state(RegisterState.phone)
        return
    await state.update_data(phone=phone)
    data = await state.get_data()

    text = (
        f"👤 Ma'lumotlaringiz:\n"
        f"• Ism: {data['name']}\n"
        f"• Familiya: {data['surname']}\n"
        f"• Yosh: {data['age']}\n"
        f"• Telefon: {data['phone']}\n\n"
        f"Ma'lumotlar to'g'rimi?"
    )

    await msg.answer(text, reply_markup=tasdiqlash_kb)
    await state.set_state(RegisterState.tasdiqlash)

@dp.message(StateFilter(RegisterState.tasdiqlash))
async def tasdiqlash_handler(msg: types.Message, state: FSMContext):
    if msg.text == "✅ Tasdiqlash":
        data = await state.get_data()
        add_user(ism=data.get("name"), familiya=data.get("surname"), yosh=data.get("age"), telefon=data.get("phone"))
        await msg.answer("Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi! 🎉", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(chat_id=ADMIN_ID, text=f"Yangi ro'yxatdan o'tgan foydalanuvchi:\n\nIsm: {data['name']}\nFamiliya: {data['surname']}\nYosh: {data['age']}\nTelefon: {data['phone']}")
        # await bot.send_message(chat_id=CHANNEL_ID, text=f"Yangi ro'yxatdan o'tgan foydalanuvchi:\n\nIsm: {data['name']}\nFamiliya: {data['surname']}\nYosh: {data['age']}\nTelefon: {data['phone']}")
        await state.clear()
    else:
        await msg.answer("Bekor qilindi ❌", reply_markup=types.ReplyKeyboardRemove())
        await msg.answer("Registratsiya uchun /register bosing") 
        await state.clear()


async def main():
    jadval_yaratish()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
