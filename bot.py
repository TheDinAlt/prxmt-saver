import asyncio
import os
from aiogram import F
from aiogram import types, Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from templates import kb, texts
from templates.states import *
from utils import config, validate_url
import downloaders

#                   INIT
dp = Dispatcher()
if config("testmode"):
    token = "test_token"
else:
    token = "main_token"
bot = Bot(token=config("main_token"), parse_mode=ParseMode.HTML)

async def start():
    print("bot started")
    await dp.start_polling(bot)


#                   DIALOGS
@dp.callback_query(F.data == 'start')
@dp.message(Command('start'))
async def start_cmd(msg: types.Message, state: FSMContext):
    await state.clear()
    user_channel_status = await bot.get_chat_member(chat_id=config("blog_id"), user_id=msg.from_user.id)
    if user_channel_status.status == 'left':
        await bot.send_message(chat_id=msg.from_user.id, text=texts.unsubscribed)
    await state.set_state(MainFSM().get_url)
    await msg.answer(text=texts.start, reply_markup=kb.start)

@dp.message(F.content_type == types.ContentType.TEXT, StateFilter(MainFSM().get_url))
async def get_url_fsm(msg: types.Message, state: FSMContext):
    r = validate_url(msg.text)
    if r is not False:
        if r["service"] == "youtube":
            info = await downloaders.Youtube().get_info(r["url"])
            m = await msg.answer(text=texts.choose_type.format("Youtube", info['title']), reply_markup=kb.choose_type)
            await state.set_data({"bot_msg_id": m.message_id,
                                  "title": info['title'],
                                  "id": info['id']})

@dp.callback_query(F.data.in_(['download_video', 'download_audio']))
async def download_cqh(cqh: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(chat_id=cqh.from_user.id, message_id=data['bot_msg_id'])
    proc_msg = await bot.send_message(chat_id=cqh.from_user.id, text=texts.proc)
    type = cqh.data.replace("download_", "")
    if type == "video":
        ext = "mp4"
    elif type == "audio":
        ext = "mp3"
    await downloaders.Youtube().download(data['id'], type=type)
    filepath = os.path.realpath(f'files\\{data["id"]}.{ext}')
    await bot.send_document(chat_id=cqh.from_user.id, 
                            document=FSInputFile(path=filepath,
                                                 filename=f'{data["title"]}.{ext}'),
                            caption=texts.made_with)
    await bot.delete_message(chat_id=cqh.from_user.id, message_id=proc_msg.message_id)
    await downloaders.delete_file(f'{data["id"]}.{ext}')