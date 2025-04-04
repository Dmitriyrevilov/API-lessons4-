import telegram
from dotenv import load_dotenv
import os
import random
import argparse
import time


load_dotenv()


def post_images_to_telegram(image_dir, interval_hours):
    API_TG_BOT = os.getenv("API_TG_BOT")
    if not API_TG_BOT:
        print("Ошибка: Не найден API_TG_BOT в переменных окружения.")
        return
    bot = telegram.Bot(token=API_TG_BOT)
    chat_id = os.getenv("TELEGRAM_CHANNEL_ID")
    if not chat_id:
        print("Ошибка: Не найден TELEGRAM_CHANNEL_ID в переменных окружения.")
        return
    try:
        chat_id = int(chat_id)
    except ValueError:
        print("Ошибка: TELEGRAM_CHANNEL_ID должен быть целым числом.")
        return
    while True:
        images = [
            os.path.join(image_dir, f)
            for f in os.listdir(image_dir)
            if f.endswith((".jpg", ".png", ".jpeg"))
        ]
        if not images:
            print(f"В директории '{image_dir}' не найдено изображений.")
            time.sleep(interval_hours * 3600)
            continue
        random.shuffle(images)
        for image in images:
            try:
                with open(image, "rb") as photo:
                    bot.send_photo(
                        chat_id=chat_id, photo=photo, caption="Фото из космоса"
                    )
                print(f"Фотография '{image}' успешно опубликована.")
            except FileNotFoundError:
                print(f"Файл не найден: {image}")
            except telegram.error.TelegramError as e:
                print(f"Ошибка при отправке фотографии '{image}': {e}")
            time.sleep(interval_hours * 3600)


def main():
    parser = argparse.ArgumentParser(
        description="Автоматическая публикация изображений в Telegram-канал."
    )
    parser.add_argument("image_dir", help="Путь к директории с изображениями.")
    parser.add_argument(
        "--interval",
        type=float,
        default=4,
        help="Интервал между публикациями в часах (по умолчанию: 4).",
    )
    args = parser.parse_args()
    post_images_to_telegram(args.image_dir, args.interval)


if __name__ == "__main__":
    main()
