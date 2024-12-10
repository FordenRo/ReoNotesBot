from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from globals import bot, session
from handlers.database import Note
from handlers.opening import open_main, open_note
from handlers.states import EditingStates

router = Router()


async def edit_note_name(note: Note, state: FSMContext):
	await state.set_state(EditingStates.note_name)
	msg = await bot.send_message(note.user.id, 'Введите новое название')
	await state.update_data(message_id=msg.message_id, note=note)


async def edit_note_desc(note: Note, state: FSMContext):
	await state.set_state(EditingStates.note_desc)
	msg = await bot.send_message(note.user.id, 'Введите новое описание')
	await state.update_data(message_id=msg.message_id, note=note)


@router.message(EditingStates.note_name)
async def process_note_name(message: Message, state: FSMContext):
	data = await state.get_data()
	await state.clear()

	await bot.delete_message(message.from_user.id, message.message_id)
	await bot.delete_message(message.from_user.id, data['message_id'])

	# note = session.scalar(select(Note).where(Note.id == data['id']))
	note = data['note']
	note.name = message.text
	session.commit()

	await open_note(note)


@router.message(EditingStates.note_desc)
async def process_note_desc(message: Message, state: FSMContext):
	data = await state.get_data()
	await state.clear()

	await bot.delete_message(message.from_user.id, message.message_id)
	await bot.delete_message(message.from_user.id, data['message_id'])

	# note = session.scalar(select(Note).where(Note.id == data['id']))
	note = data['note']
	note.description = message.text
	session.commit()

	await open_note(note)