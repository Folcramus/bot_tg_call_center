from aiogram import Bot, Dispatcher, types, F
import asyncio
import logging
import sys
import os
from dotenv import load_dotenv, find_dotenv
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.fsm.storage.memory import MemoryStorage
from func import CreateElement, UpdateElement, GetElement, GetElementChatUser, GetElementIdTopicChat, UpdateoOperatorElement, GetElementChat2User
from classesBot import MyDialog
from conf import Connect
from aiogram.fsm.context import FSMContext

load_dotenv(find_dotenv())
lex_imper = list()
chat_topic_id = ""
bot = Bot(os.getenv("TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def process_start_command(message: types.Message, state: FSMContext):
    if GetElement(message.from_user.id) is not None:
        await message.answer(
            "Здравствуйте! Пожалуйста задайте Ваш вопрос оператору. На ваше обращение ответит первый освободившийся "
            "оператор (рабочее время 07:00 - 18:00 без выходных)")
    else:
        kb = [
            [types.KeyboardButton(text="Поделится номером", request_contact=True)]
        ]
        board = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer("Здравствуйте! Нажмите на кнопку поделится номером", reply_markup=board)
        await state.set_state(MyDialog.otvet)



@dp.message(F.chat.id == -1001842118341)
async def send_topics(message: types.Message, state: FSMContext):
    if message.text is not None:
        print(message.message_thread_id)
        res = GetElementChat2User(message.message_thread_id)
        await bot.send_message(res[0], message.text, disable_web_page_preview=True)
    if message.photo is not None:
        res = GetElementChat2User(message.from_user.id)
        photos = message.photo
        await bot.send_photo(res[0], photos[-1].file_id)


@dp.message(F.contact)
async def Topics(message: types.Message, state: FSMContext):
    contact = message.contact
    CreateElement(contact.phone_number, message.from_user.full_name + contact.phone_number, message.from_user.id,
                  message.chat.id, message.from_user.full_name, 0)
    topic = await bot.create_forum_topic(-1001842118341, message.from_user.full_name + " " + contact.phone_number)
    UpdateElement(message.from_user.id, topic.message_thread_id)
    await message.answer(
        "Здравствуйте! Пожалуйста задайте Ваш вопрос оператору. На ваше обращение ответит первый освободившийся "
        "оператор (рабочее время 07:00 - 18:00 без выходных)")






@dp.message()
async def Sender(message: types.Message):
    if GetElementChatUser(message.from_user.id) is not None:
        res0 = GetElementChatUser(message.from_user.id)
        if res0[0] == message.chat.id:
            res1 = GetElementIdTopicChat(message.from_user.id)
            photos = message.photo
            if photos is None and message.text is not None:
                await bot.send_message(-1001842118341, message.text, message_thread_id=res1[0],
                                       disable_web_page_preview=True)
            elif photos is not None:
                await bot.send_photo(-1001842118341, photos[-1].file_id, message_thread_id=res1[0])
    else:
        kb = [
            [types.KeyboardButton(text="Поделится номером", request_contact=True)]
        ]
        board = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer("Для того чтобы начать общение с оператором, нажмите на кнопку поделится номером", reply_markup=board)


@dp.message()
async def main() -> None:
    await  dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
