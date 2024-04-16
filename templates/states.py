from aiogram.fsm.state import StatesGroup, State

class MainFSM(StatesGroup):
    not_subscribed = State()
    get_url = State()