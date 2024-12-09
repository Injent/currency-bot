from typing import Final

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message

from config_data.config import config
from database.methods.user import change_user_base_currency
from handlers.menu import answer_with_menu
from keyboards.keyboards_utils import create_currencies_keyboard
from states.states import MenuState

CALLBACK_CHANGE_CURRENCY: Final[str] = 'change_base_currency'


router = Router()


@router.callback_query(F.data == 'settings')
async def settings(callback: CallbackQuery, state: FSMContext):
    await answer_with_settings(callback.message)
    await state.set_state(MenuState.idle)


@router.callback_query(MenuState.idle, F.data == CALLBACK_CHANGE_CURRENCY)
async def change_base_currency(callback: CallbackQuery, state: FSMContext):
    keyboard = create_currencies_keyboard(config.currencies)
    await callback.message.answer(
        text='Впишите название валюты в таком формате: RUB, USD и т.д.',
        reply_markup=keyboard
    )
    await state.set_state(MenuState.pending_for_symbol)


@router.callback_query(MenuState.idle, F.data == 'back')
async def back(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await answer_with_menu(callback.message)


@router.message(MenuState.pending_for_symbol)
async def on_input_symbol(message: Message, state: FSMContext):
    if message.text in config.currencies:
        await state.set_state(MenuState.idle)
        await change_user_base_currency(message.from_user.id, message.text)
        await answer_with_settings(message)
    else:
        await message.answer(text='Такой валюты не существует, попробуйте снова')


def answer_with_settings(message: Message) -> SendMessage:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Поменять базовую валюту', callback_data=CALLBACK_CHANGE_CURRENCY)],
            [InlineKeyboardButton(text='Назад', callback_data='back')]
        ]
    )
    return message.answer(text='⚙️ Настройки\n\nНастройте базовый курс валюты здесь', reply_markup=keyboard)