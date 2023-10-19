from aiogram import Bot, Dispatcher, types, F
import asyncio
import logging
import sys
import os
from dotenv import load_dotenv, find_dotenv
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.fsm.storage.memory import MemoryStorage
from func import CreateElement, UpdateElement, GetElement, GetElementChatUser, GetElementIdTopicChat, \
    GetPhoneElement, GetElementChat2User, UpdatePhoneElement
from GoogleTableFunc import GetPhoneTable
from classesBot import MyDialog
from aiogram.fsm.context import FSMContext

load_dotenv(find_dotenv())
bot = Bot(os.getenv("TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def process_start_command(message: types.Message):
    if GetElement(message.from_user.id) is not None:
        await message.answer(
            "✅ Спасибо за предоставленную информацию! Задайте, пожалуйста, ваш вопрос. Первый освободившийся оператор "
            "ответит на ваше обращение в рабочее время с 09:00 до 21:00 без выходных.")
    else:
        kb = [
            [types.KeyboardButton(text="Ввести номер")]
        ]
        board = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Здравствуйте! Для того чтобы начать общение с оператором, нажмите на кнопку "Ввести номер"', reply_markup=board)


@dp.message(F.text.lower() == 'ввести номер')
async def Topics(message: types.Message, state: FSMContext):
    await message.answer("🔒 Для идентификации введите, пожалуйста, номер телефона, который вы указали при заключении договора. Формат: 7XXXXXXXXXX Пример: 79991234567", reply_markup=types.ReplyKeyboardRemove() )
    await state.set_state(MyDialog.otvet)


@dp.message(MyDialog.otvet)
async def Mes(message: types.Message, state: FSMContext):
    if len(message.text) == 11 and "7" in message.text:

        if GetPhoneElement(message.text) is not None:
            UpdatePhoneElement(message.from_user.id, message.text)
        else:
            CreateElement(message.text, message.from_user.full_name + message.text, message.from_user.id,
                          message.chat.id, message.from_user.full_name, 0)
            googletable = GetPhoneTable(int(message.text))
            if googletable is not None:
                numb_order = str(googletable['Номер заказа'])
                topic = await bot.create_forum_topic(int(os.getenv("ID")), f"{googletable['Номер телефона']}  № {numb_order}  {googletable['ФИО']}")
                UpdateElement(message.from_user.id, topic.message_thread_id)
            else:
                phone = GetPhoneElement(message.text)
                topic = await bot.create_forum_topic(int(os.getenv("ID")),
                                                     f"Без № заказа  {message.from_user.full_name} {phone[1]}")
                UpdateElement(message.from_user.id, topic.message_thread_id)
        await message.answer(
                "✅ Спасибо за предоставленную информацию! Задайте, пожалуйста, ваш вопрос. Первый освободившийся оператор "
            "ответит на ваше обращение в рабочее время с 09:00 до 21:00 без выходных.")
        await state.clear()
    else:
        await message.answer(
                "Номер введен неправильно. Введите номер телефона в формате 7ХХХХХХХХХХ Пример: 79991234567")


@dp.message(F.chat.id == int(os.getenv("ID")))
async def send_topics(message: types.Message):
    if message.text is not None:
        res = GetElementChat2User(message.message_thread_id)
        await bot.send_message(res[0], message.text, disable_web_page_preview=True)
    if message.photo is not None:
        res = GetElementChat2User(message.message_thread_id)
        photos = message.photo
        await bot.send_photo(res[0], photos[-1].file_id)


@dp.message()
async def Sender(message: types.Message):
    if GetElementChatUser(message.from_user.id) is not None:
        res0 = GetElementChatUser(message.from_user.id)
        if res0[0] == message.chat.id:
            res1 = GetElementIdTopicChat(message.from_user.id)
            photos = message.photo
            if photos is None and message.text is not None:
                await bot.send_message(int(os.getenv("ID")), message.text, message_thread_id=res1[0],
                                       disable_web_page_preview=True)
            elif photos is not None:
                await bot.send_photo(int(os.getenv("ID")), photos[-1].file_id, message_thread_id=res1[0])
    else:
        kb = [
            [types.KeyboardButton(text="Ввести номер")]
        ]
        board = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Для того чтобы начать общение с оператором, нажмите на кнопку "Ввести номер"',
                             reply_markup=board)


@dp.message()
async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %('
                                                                      'message)s')
    asyncio.run(main())
