from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Заметка', callback_data='create_note')],
													[InlineKeyboardButton(text='Папка', callback_data='create_folder')]])


def get_link_button(text: str, data: str):
	return f'<a href="t.me/reonotesbot?start={data}">{text}</a>'