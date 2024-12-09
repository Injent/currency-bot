from aiogram import Router, F
from aiogram.types import CallbackQuery

from config_data.config import config
from database.methods.user import get_user_base_currency
from external_services.currencyapi import get_currency_rates
from handlers.menu import answer_with_menu

router = Router()


@router.callback_query(F.data == 'view_currency')
async def view_currency(callback: CallbackQuery):
    user_base_currency: str = await get_user_base_currency(callback.from_user.id)

    currencies = config.currencies.copy()
    currencies.remove(user_base_currency)
    rates: dict[str, float] = await get_currency_rates(base=user_base_currency, symbols=currencies)

    formatted_string = f'Текущий курс {user_base_currency}:\n'

    for symbol in rates.keys():
        value = rates[symbol]
        formatted_string += f'\n{symbol} = {value} {user_base_currency}'

    await callback.message.answer(text=formatted_string)
    await answer_with_menu(callback.message)