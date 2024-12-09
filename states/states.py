from aiogram.fsm.state import StatesGroup, State

last_message: dict[int, int]

class CalculatorState(StatesGroup):
    pending_from_currency = State()
    pending_to_currency = State()
    pending_currency_value = State()
    check_cur = State()


class MenuState(StatesGroup):
    idle = State()
    pending_for_symbol = State()