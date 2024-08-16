from selenium import webdriver
from dotenv import load_dotenv
from approveContract import approveContract
import logging, os, asyncio, sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')

driver = webdriver.Chrome()
driver.set_window_size(1200, 800)
driver.get('https://1sed.infogeneral.ru/auth/login')

dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer("Напишите список id договор в строку по одному!")

@dp.message()
async def contracts_hanlder(message: Message) -> None:
    contracts = []
    for line in message.text.splitlines():
        if await approveContract(driver, line):
            contracts.append(line + " - согласован \n")
        else:
            contracts.append(line + " - Не найден либо не состоит группе \n")
    resultMessage = ''.join(map(str, contracts))
    
    await message.answer(resultMessage)
    

async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) 
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
