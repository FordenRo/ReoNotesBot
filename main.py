from asyncio import run as run_async

from aiogram import Dispatcher

from globals import bot, engine, session
from handlers import start, creation, editing
from handlers.database import Base

dispatcher = Dispatcher()


async def main():
	Base.metadata.create_all(engine)

	dispatcher.include_routers(start.router,
							   creation.router,
							   editing.router)

	await dispatcher.start_polling(bot)
	await session.commit()
	await engine.dispose()


if __name__ == '__main__':
	run_async(main())
