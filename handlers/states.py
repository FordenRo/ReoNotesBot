from aiogram.fsm.state import StatesGroup, State


class EditingStates(StatesGroup):
	note_name = State()
	note_desc = State()