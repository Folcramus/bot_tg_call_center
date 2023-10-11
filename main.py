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
            "Здравствуйте! Пожалуйста задайте Ваш вопрос оператору. На ваше обращение ответит первый освободившийся "
            "оператор (рабочее время 07:00 - 18:00 без выходных)")
    else:
        kb = [
            [types.KeyboardButton(text="Ввести номер")]
        ]
        board = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer("Здравствуйте! Нажмите на кнопку Ввести номер", reply_markup=board)


@dp.message(F.text.lower() == 'ввести номер')
async def Topics(message: types.Message, state: FSMContext):
    await message.answer("Введите номер телефона указанный Вами при заключении договора в формате +7ХХХХХХХХХХ")
    await state.set_state(MyDialog.otvet)


@dp.message(MyDialog.otvet)
async def Mes(message: types.Message, state: FSMContext):
    if len(message.text) == 12 and "+" in message.text:

        if GetPhoneElement(message.text) is not None:
            UpdatePhoneElement(message.from_user.id, message.text)
        else:
            CreateElement(message.text, message.from_user.full_name + message.text, message.from_user.id,
                          message.chat.id, message.from_user.full_name, 0)
            googletable = GetPhoneTable(int(message.text[1::]))
            if googletable is not None:
                numb_order = str(googletable['Номер заказа'])
                topic = await bot.create_forum_topic(int(os.getenv("ID")), f"{googletable['Имя']} № {numb_order}")
                UpdateElement(message.from_user.id, topic.message_thread_id)
            else:
                phone = GetPhoneElement(message.text)
                topic = await bot.create_forum_topic(int(os.getenv("ID")),
                                                     f"Без № заказа  {message.from_user.full_name} {phone[1]}")
                UpdateElement(message.from_user.id, topic.message_thread_id)
        await message.answer(
                "Здравствуйте! Пожалуйста задайте Ваш вопрос оператору. На ваше обращение ответит первый освободившийся"
                "оператор (рабочее время 07:00 - 18:00 без выходных)")
        await state.clear()
    else:
        await message.answer(
                "Номер введен неправильно. Введите номер телефона в формате +7ХХХХХХХХХХ")


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
            [types.KeyboardButton(text="Ввести номер", request_contact=True)]
        ]
        board = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer("Для того чтобы начать общение с оператором, нажмите на кнопку поделится номером",
                             reply_markup=board)


@dp.message()
async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %('
                                                                      'message)s')
    asyncio.run(main())
