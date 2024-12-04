import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from save import *
from data import *


dp = Dispatcher()
D = D()

class Form(StatesGroup):
    new_data = State()

inline_kb = InlineKeyboardBuilder()
inline_kb.button(text='Предложить изменения', callback_data='but_suggestchanges')
inline_kb.button(text='ДЗ', callback_data='but_print')
inline_kb.button(text='Ссылки', callback_data='but_links')
keyboard_user = inline_kb.as_markup()

inline_kb = InlineKeyboardBuilder()
inline_kb.button(text='Измененить', callback_data='but_redact')
inline_kb.button(text='ДЗ', callback_data='but_print')
inline_kb.button(text='Ссылки', callback_data='but_links')
inline_kb.button(text='Предложка', callback_data='but_peek')
keyboard_admin = inline_kb.as_markup()

inline_kb = InlineKeyboardBuilder()
inline_kb.button(text='clear', callback_data='clear')
keyboard_clear = inline_kb.as_markup()

inline_kb_select = InlineKeyboardBuilder()
for i in D.subjects:
    inline_kb_select.row(InlineKeyboardButton(text=i, callback_data='select_' + i))
keybord_select = inline_kb_select.as_markup()


@dp.message(lambda message: message.text and message.text.lower() == '/print_data')
async def print_arr(message: Message):
    read_save()
    ss = ""
    for key, value in D.data.items():
        ss += str(key) + ": " + str(value) + "\n\n" 
    await bot.send_message(chat_id=message.chat.id, text=ss)


@dp.message(lambda message: message.text and message.text.lower() == '/clear_data')
async def clear_data(message: Message):
    clear()
    await bot.send_message(chat_id=message.chat.id, text="clear")


async def print_suggestion(message: Message):
    read_save()
    ss = ""
    for i in D.suggestion:
        ss +=  i + "\n"
    if (ss == ""):
        await bot.send_message(chat_id=message.chat.id, text="no suggestion")
    else:
        await message.answer(ss, reply_markup=keyboard_clear)

async def print_links(message: Message):
    await message.answer(str(D.links))
    


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if (message.from_user.id != D.adminId):
        await message.answer(f"Что вы хотите сделать с данными?", reply_markup=keyboard_user)
    else:
        await message.answer(f"Что вы хотите сделать с данными создатель? ", reply_markup=keyboard_admin)

@dp.message(lambda message: message.text and message.text.lower() == '/edit')
async def edit(message: Message) -> None:
    read_save()  
    await message.answer(f"Выбери предмет", reply_markup=keybord_select)


@dp.callback_query(lambda query: query.data.startswith("clear"))
async def clear_suggestion(call: CallbackQuery):
    D.suggestion = []
    edit_save()
    await call.message.answer("cleared")
    await call.message.delete()
    await call.answer()


@dp.callback_query(lambda query: query.data.startswith("select"))
async def select_button(call: CallbackQuery, state: FSMContext):
    await state.update_data(subject=call.data.split("_")[-1]) 
    await state.set_state(Form.new_data)
    await call.message.delete()
    temp_data = await state.get_data()
    subject = temp_data['subject']
    await call.message.answer(str(subject) + ": продолжи в формате дд дз")
    await call.answer()


@dp.message(Form.new_data)
async def new_text_handler(message: Message, state: FSMContext):
    temp_data = await state.get_data()
    subject = temp_data['subject']
    new_text = message.text
    if (new_text != ""):
        if (message.from_user.id == D.adminId):
            D.data[subject] = new_text
            edit_save()
            await print_arr(message)
        else:
            D.suggestion.append(str(message.from_user.full_name) + " " + str(subject) + ": " + new_text)
            edit_save()
            await bot.send_message(chat_id=message.chat.id, text="Ваше предложение занисано\nОно будет добавлено после проверки")
    await state.clear()



@dp.callback_query(lambda query: query.data.startswith("but"))
async def process_callback(callback_query: types.CallbackQuery):
    com = callback_query.data.split("_")[-1]
    if com == "redact" or com == "suggestchanges":
        await edit(callback_query.message)
    if com == "print":
        await print_arr(callback_query.message)
    if com == "peek":
        await print_suggestion(callback_query.message)
    if com == "links":
        await print_links(callback_query.message)
    
    await callback_query.message.delete()
    await callback_query.answer()


async def main() -> None:
    global bot
    bot = Bot(D.TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    