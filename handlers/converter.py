from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

from config_data.config import config
from external_services.currencyapi import convert_currency
from handlers.menu import answer_with_menu
from keyboards.keyboards_utils import create_currencies_keyboard
from states.states import CalculatorState

router = Router()


@router.callback_query(F.data == 'convert')
async def select_from_cur(callback: CallbackQuery, state: FSMContext):
    cur_keyboard = create_currencies_keyboard(config.currencies)
    await state.set_state(CalculatorState.pending_from_currency)
    await callback.message.answer(text='Выберите какую валюту хотите перевести:', reply_markup=cur_keyboard)


@router.message(CalculatorState.pending_from_currency)
async def on_from_currency_input(message: Message, state: FSMContext):
    if message.text not in config.currencies:
        await message.answer(
            text='Введенное значение не является валютой. Попробуй еще раз',
            reply_markup=create_currencies_keyboard(config.currencies)
        )
        return
    await state.set_state(CalculatorState.pending_currency_value)
    await state.update_data({'from': message.text})
    await message.answer(text='Введите количество выбранной валюты:', reply_markup=ReplyKeyboardRemove())


@router.message(CalculatorState.pending_currency_value, F.text)
async def on_currency_value_input(message: Message, state: FSMContext):
    if not isint(message.text):
        await message.answer('Это не число')
        return

    data = await state.get_data()
    await state.set_state(CalculatorState.pending_to_currency)
    await state.update_data({'amount': int(message.text)})
    # Копируем список существующих валют и убераем уже выбранную валюту
    currencies = config.currencies.copy()
    currencies.remove(data['from'])
    cur_keyboard = create_currencies_keyboard(currencies)
    await message.answer('Теперь выберите в какую валюту хотите перевести:', reply_markup=cur_keyboard)


@router.message(CalculatorState.pending_to_currency)
async def on_to_currency_input(message: Message, state: FSMContext):
    data = await state.get_data()
    from_cur: str = data['from']
    to_cur = message.text
    if to_cur not in config.currencies:
        currencies = config.currencies.copy()
        currencies.remove(from_cur)
        cur_keyboard = create_currencies_keyboard(currencies)
        await message.answer(text='Введеное значение не является валютой. Попробуй заново', reply_markup=cur_keyboard)
        return

    amount: int = data['amount']

    result = await convert_currency(base=from_cur, to=to_cur, amount=amount)
    await message.answer(text=f'{amount} {from_cur} = {result} {to_cur}', reply_markup=ReplyKeyboardRemove())
    await state.set_state(None)
    await state.set_data({})
    await answer_with_menu(message)


def isint(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_base_keyboard() -> InlineKeyboardMarkup:
    convert_btn = InlineKeyboardButton(text='Конвертировать', callback_data='convert')
    check_btn = InlineKeyboardButton(text='Посмотреть курс', callback_data='check_cur')
    return InlineKeyboardMarkup(inline_keyboard=[[convert_btn, check_btn]])