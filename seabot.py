import asyncio


from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from save import *

adminId = 1335525100
TOKEN = "6167485884:AAFchWRaQomUHPcZMQyclK_9KzXhEgAAW1Y"
data = {"матан": "", "линал": "", "forFun": ""}
suggestion = []
dp = Dispatcher()


class Form(StatesGroup):
    new_data = State()
    new_data_suggestion = State()

inline_kb = InlineKeyboardBuilder()
inline_kb.button(text='Предложить изменения', callback_data='but_suggestchanges')
inline_kb.button(text='Получить', callback_data='but_print')
keyboard_user = inline_kb.as_markup()

inline_kb = InlineKeyboardBuilder()
inline_kb.button(text='Измененить', callback_data='but_redact')
inline_kb.button(text='Получить', callback_data='but_print')
inline_kb.button(text='Предложка', callback_data='but_peek')
keyboard_admin = inline_kb.as_markup()

inline_kb = InlineKeyboardBuilder()
inline_kb.button(text='матан', callback_data='select_матан')
inline_kb.button(text='линал', callback_data='select_линал')
inline_kb.button(text='forFun', callback_data='select_forFun')
keyboard1 = inline_kb.as_markup()

inline_kb = InlineKeyboardBuilder()
inline_kb.button(text='матан', callback_data='suggestion_матан')
inline_kb.button(text='линал', callback_data='suggestion_линал')
inline_kb.button(text='forFun', callback_data='suggestion_forFun')
keyboard_suggestion = inline_kb.as_markup()

inline_kb = InlineKeyboardBuilder()
inline_kb.button(text='clear', callback_data='clear')
keyboard_clear = inline_kb.as_markup()


@dp.message(lambda message: message.text and message.text.lower() == '/print_data')
async def print_arr(message: Message):
    global data, suggestion
    data, suggestion = read_save()
    ss = ""
    for key, value in data.items():
        ss += str(key) + ": " + str(value) + "\n"
    await bot.send_message(chat_id=message.chat.id, text=ss)


async def print_suggestion(message: Message):
    global data, suggestion
    data, suggestion = read_save()
    ss = ""
    for i in suggestion:
        ss +=  i + "\n"
    if (ss == ""):
        await bot.send_message(chat_id=message.chat.id, text="no suggestion")
    else:
        await message.answer(ss, reply_markup=keyboard_clear)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if (message.from_user.id != adminId):
        await message.answer(f"Что вы хотите сделать с данными?", reply_markup=keyboard_user)
    else:
        await message.answer(f"Что вы хотите сделать с данными создатель? ", reply_markup=keyboard_admin)

@dp.message(lambda message: message.text and message.text.lower() == '/edit')
async def edit(message: Message) -> None:
    global data, suggestion
    data, suggestion = read_save()     
    await message.answer(f"Выбери предмет", reply_markup=keyboard1)


async def edit_suggestion(message: Message) -> None: 
    global data, suggestion
    data, suggestion = read_save()     
    await message.answer(f"Выбери предмет", reply_markup=keyboard_suggestion)


@dp.callback_query(lambda query: query.data.startswith("clear"))
async def clear_suggestion(call: CallbackQuery):
    global data, suggestion
    suggestion = []
    edit_save(data, suggestion)
    await call.message.answer("cleared")
    await call.answer()


@dp.callback_query(lambda query: query.data.startswith("select"))
async def select_button(call: CallbackQuery, state: FSMContext):
    await state.update_data(subject=call.data.split("_")[-1]) 
    await state.set_state(Form.new_data)
    await call.message.answer("Введите текст:")
    await call.answer()


@dp.callback_query(lambda query: query.data.startswith("suggestion"))
async def select_button_suggestion(call: CallbackQuery, state: FSMContext):
    global suggestion
    await state.update_data(subject=call.data.split("_")[-1]) 
    await state.set_state(Form.new_data_suggestion)
    await call.message.answer("Введите текст:")
    await call.answer()


@dp.message(Form.new_data)
async def new_text_handler(message: Message, state: FSMContext):
    global data, suggestion
    temp_data = await state.get_data()
    subject = temp_data['subject']
    new_text = message.text
    data[subject] = new_text
    edit_save(data, suggestion)
    await print_arr(message)
    await state.clear()


@dp.message(Form.new_data_suggestion)
async def new_text_handler_suggestion(message: Message, state: FSMContext):
    global suggestion, data
    temp_data = await state.get_data()
    subject = temp_data['subject']
    new_text = message.text
    print(message.from_user.id)
    suggestion.append(str(message.from_user.full_name) + " " + str(subject) + ": " + new_text)
    edit_save(data, suggestion)
    await bot.send_message(chat_id=message.chat.id, text="Ваше предложение занисано\nОно будет добавлено после проверки")
    await state.clear()


@dp.callback_query(lambda query: query.data.startswith("but"))
async def process_callback(callback_query: types.CallbackQuery):
    global data
    com = callback_query.data.split("_")[-1]
    if com == "redact":
        await edit(callback_query.message)
    if com == "print":
        await print_arr(callback_query.message)
    if com == "suggestchanges":
        await edit_suggestion(callback_query.message)
    if com == "peek":
        await print_suggestion(callback_query.message)
    await callback_query.answer()


async def main() -> None:
    global bot
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())