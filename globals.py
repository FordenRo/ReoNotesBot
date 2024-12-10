from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

TOKEN = '7955354178:AAECXeMK9T_3ogXe0ZeVlwP43qWLMQCxlJ0'
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
engine = create_engine('sqlite:///database.db')
session = Session(engine)