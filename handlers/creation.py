from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select

from globals import session
from handlers.database import Note, User, Folder
from handlers.opening import open_main

router = Router()


@router.callback_query(F.data == 'create_note')
async def create_note(callback: CallbackQuery):
	user = session.scalar(select(User).where(User.id == callback.from_user.id))

	note = Note(name='Unnamed', user=user)
	session.add(note)
	session.commit()

	await open_main(user)


@router.callback_query(F.data == 'create_folder')
async def create_folder(callback: CallbackQuery):
	user = session.scalar(select(User).where(User.id == callback.from_user.id))

	folder = Folder(name='Unnamed folder', user=user)
	session.add(folder)
	session.commit()

	await open_main(user)