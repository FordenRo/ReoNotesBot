from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import exists, select

from globals import bot, session
from handlers.database import User, Note, Folder
from handlers.editing import edit_note_name, edit_note_desc
from handlers.opening import open_note, expand_folder, open_main
from utils import get_link_button, main_markup

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
	await message.delete()

	if session.query(exists(User).where(User.id == message.chat.id)).scalar():
		print(message.text)
		args = message.text.removeprefix('/start').strip().split('-')
		if not args:
			pass
		elif args[0] == 'main':
			user = session.scalar(select(User).where(User.id == message.chat.id))
			await open_main(user)
		elif args[0] == 'note':
			id = int(args[1])
			note = session.scalar(select(Note).where(Note.id == id))
			await open_note(note)
		elif args[0] == 'folder':
			id = int(args[1])
			folder = session.scalar(select(Folder).where(Folder.id == id))
			await expand_folder(folder)
		elif args[0] == 'edit':
			if args[1] == 'note':
				id = int(args[3])
				note = session.scalar(select(Note).where(Note.id == id))
				if args[2] == 'name':
					await edit_note_name(note, state)
				elif args[2] == 'desc':
					await edit_note_desc(note, state)
	else:
		user = User(id=message.chat.id)
		session.add(user)
		session.commit()

		user.message_id = (await bot.send_message(user.id,
												  'Добро пожаловать!',
												  reply_markup=InlineKeyboardMarkup(
													  inline_keyboard=[[InlineKeyboardButton(
														  text='Создать заметку',
														  callback_data='create_note')]]))).message_id
