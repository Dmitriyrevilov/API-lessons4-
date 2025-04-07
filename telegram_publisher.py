import telegram
from dotenv import load_dotenv
import os
import random
import argparse
import time
from telegram.error import TelegramError
from requests.exceptions import RequestException


def send_image_to_telegram(bot, chat_id, image_path):
    with open(image_path, "rb") as photo:
        bot.send_photo(chat_id=chat_id, photo=photo, caption="Фото из космоса")
    print(f"Фотография '{image_path}' успешно опубликована.")


def post_images_to_telegram(
    image_dir, interval_hours, telegram_bot_token, telegram_channel_id
):
    bot = telegram.Bot(token=telegram_bot_token)
    images = [
        os.path.join(image_dir, f)
        for f in os.listdir(image_dir)
        if f.endswith((".jpg", ".png", ".jpeg"))
    ]
    if not images:
        print(f"В директории '{image_dir}' не найдено изображений.")
        time.sleep(interval_hours * 3600)
        return
    random.shuffle(images)
    for image in images:
        send_image_to_telegram(bot, telegram_channel_id, image)
        time.sleep(interval_hours * 3600)


def main():
    load_dotenv()
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
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_bot_token:
        print("Ошибка: Не найден TELEGRAM_BOT_TOKEN в переменных окружения.")
        return
    telegram_channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    if not telegram_channel_id:
        print("Ошибка: Не найден TELEGRAM_CHANNEL_ID в переменных окружения.")
        return
    try:
        telegram_channel_id = int(telegram_channel_id)
        post_images_to_telegram(
            args.image_dir, args.interval, telegram_bot_token, telegram_channel_id
        )
    except ValueError:
        print("Ошибка: TELEGRAM_CHANNEL_ID должен быть целым числом.")
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    except TelegramError as e:
        print(f"Ошибка при отправке фотографии: {e}")
    except OSError as e:
        print(f"Ошибка файловой системы: {e}")
    except RequestException as e:
        print(f"Ошибка сетевого подключения: {e}")


if __name__ == "__main__":
    main()
