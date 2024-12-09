from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database.methods.user import register_user

router = Router()


@router.message(CommandStart())
async def on_start(message: Message):
    await register_user(user_id=message.from_user.id)
    await answer_with_menu(message)


@router.callback_query(F.data == 'back_to_menu')
async def menu(callback: CallbackQuery):
    await answer_with_menu(callback.message)


async def answer_with_menu(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🤖 О боте', callback_data='about')],
            [InlineKeyboardButton(text='⚙️ Настройки', callback_data='settings')],
            [InlineKeyboardButton(text='💱 Конвертировать', callback_data='convert')],
            [InlineKeyboardButton(text='📈 Смотреть курс', callback_data='view_currency')]
        ]
    )
    await message.answer(
        text='📜 МЕНЮ\n\n💱 Для выбора просмотра курса выберите основную валюту в настройках\n',
        reply_markup=keyboard
    )