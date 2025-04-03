import telegram
from dotenv import load_dotenv
import os



from download_apod import download_apod_images 
from download_epic import download_epic_images
from fetch_spacex_images import fetch_spacex_images
from coolprogram import download_image






load_dotenv()


API_TG_BOT = os.getenv("API_TG_BOT")
bot = telegram.Bot(token=API_TG_BOT)

chat_id = bot.get_updates()[-1].message.chat_id


bot.send_message(chat_id=chat_id, text="Привет")

try:
    with open("image.jpg", "rb") as photo:
        bot.send_photo(chat_id=chat_id, photo=photo, caption="Фото из космоса")
    print("Фотография успешно отправлена!")