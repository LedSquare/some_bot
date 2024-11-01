from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from approveContract import approveContract
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import logging, os, asyncio, re, sys

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1400,900")

if os.getenv('ENV') == 'prod':
    options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
driver.get('https://1sed.infogeneral.ru/auth/login')

dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer("Напишите список id договор в строку по одному!")

@dp.message()
async def contracts_hanlder(message: Message) -> None:
    contracts = []
    numbers = await prepare_message(message.text)
    for line in numbers:
        if await approveContract(driver, line):
            contracts.append(line + " - согласован \n")
        else:
            contracts.append(line + " - Не найден либо не находится в группе \n")
    resultMessage = ''.join(map(str, contracts))
    
    await message.answer(resultMessage)
    

async def prepare_message(message: str) -> list[str]:
    cleaned_message = re.sub(r'[^\d]', '', message)
    numbers = [cleaned_message[i:i+6] for i in range(0, len(cleaned_message), 6)]
    return numbers

async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) 
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
