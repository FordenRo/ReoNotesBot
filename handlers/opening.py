from globals import bot, session
from handlers.database import User, Note, Folder
from utils import get_link_button, main_markup


async def open_main(user: User):
	if user.notes:
		strings = ['[Главная]\n']
		for folder in user.folders:
			if folder.parent:
				continue

			strings += [get_link_button(('> ' if folder.folded else '^ ') + folder.name, f'folder-{folder.id}')]

			if not folder.folded:
				for note in folder.notes:
					if note.folder is not folder:
						continue

					strings += ['  ' + get_link_button(note.name, f'note-{note.id}')]

		strings += [get_link_button(note.name, f'note-{note.id}') for note in user.notes if not note.folder]

		await bot.edit_message_text(
			'\n'.join(strings),
			chat_id=user.id,
			message_id=user.message_id,
			reply_markup=main_markup)
	else:
		await bot.edit_message_text('У вас нет заметок',
									chat_id=user.id,
									message_id=user.message_id,
									reply_markup=main_markup)


async def open_note(note: Note):
	user = note.user
	path = [get_link_button('Главная', 'main')]
	if note.folder:
		path += [note.folder.name]
	path += ['Заметки']

	strings = [f'[{'/'.join(path)}]\n',
			   get_link_button(f'<b>{note.name}</b>', f'edit-note-name-{note.id}'),
			   get_link_button('Описание' if note.description else 'Нет описания', f'edit-note-desc-{note.id}') + (f': {note.description}' if note.description else '')]

	await bot.edit_message_text('\n'.join(strings),
								chat_id=user.id,
								message_id=user.message_id)


async def expand_folder(folder: Folder):
	folder.folded = not folder.folded

	await open_main(folder.user)