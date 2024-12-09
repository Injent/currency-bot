from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

router = Router()


@router.callback_query(F.data == 'about')
async def about(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='OK',callback_data='back_to_menu')]]
    )
    await callback.message.answer(
        text='Бот умеет переводить из одной валюты в другую и предоставлять актуальный курс на основе выбранной валюты',
        reply_markup=keyboard
    )
