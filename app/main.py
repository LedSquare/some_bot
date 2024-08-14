from selenium import webdriver
from dotenv import load_dotenv
from approveContract import approveContract
import telebot
import logging, os

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

driver = webdriver.Chrome()
driver.set_window_size(1200,800)
driver.get('https://1sed.infogeneral.ru/auth/login')

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, "Напишите список id договор в строку по одному!")

@bot.message_handler(content_types=['text'])
def get_contracts(message):
    contracts = ''
    for line in message.text.splitlines():
        # if approveContract(driver, line):
        contracts = contracts.join(line + " - Согласован\n")

        print(contracts)
        # else:
            # contracts = contracts.join(line + " - Не найден либо не состоит группе\n")
    # bot.send_message(message.chat.id, contracts)


def main() -> None:
    bot.infinity_polling()
    
if __name__ == '__main__':
    main()
