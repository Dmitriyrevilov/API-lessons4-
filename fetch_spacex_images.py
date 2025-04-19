import requests
import os
import argparse
from coolprogram import download_image
from urllib.error import URLError
from requests.exceptions import RequestException


def get_spacex_info(flight_id):
    launch_url = f"https://api.spacexdata.com/v5/launches/{flight_id}"
    response = requests.get(launch_url)
    response.raise_for_status()
    return response.json()


def get_flight_id(flight_id_arg=None, default_flight_id=None):
    flight_id = flight_id_arg or default_flight_id
    if not flight_id:
        last_launch = get_spacex_info("latest")
        flight_id = last_launch["id"]
    return flight_id


def fetch_spacex_images(flight_id):
    launch_info = get_spacex_info(flight_id)
    urls_image = launch_info["links"]["flickr"]["original"]
    if not urls_image:
        print(f"Нет изображений для запуска с ID: {flight_id}")
        return []
    os.makedirs("images_spacex", exist_ok=True)
    downloaded_images = []
    for image_number, image_url in enumerate(urls_image):
        filename = f"spacex_{image_number}.jpeg"
        filepath = os.path.join("images_spacex", filename)
        success = download_image(image_url, filepath)
        if success:
            downloaded_images.append(image_url)
        else:
            print(f"Не удалось скачать изображение {image_url}")
    return downloaded_images


def main():
    SPACEX_FLIGHT_ID = os.getenv("SPACEX_FLIGHT_ID")
    SPACEX_IMAGES_DIR = os.getenv("SPACEX_IMAGES_DIR", "images_spacex")
    parser = argparse.ArgumentParser(
        description="Скачивает изображения с запуска SpaceX. Если ID не указан, скачивает последний запуск."
    )
    parser.add_argument("--flight_id", help="ID запуска SpaceX.")
    
    parser.add_argument(
        "--directory",
        default=SPACEX_IMAGES_DIR,
        help=f"Директория для сохранения изображений (по умолчанию: {SPACEX_IMAGES_DIR}, или переменная окружения SPACEX_IMAGES_DIR)",
    )
    args = parser.parse_args()
    default_flight_id = SPACEX_FLIGHT_ID
    try:
        flight_id = get_flight_id(args.flight_id, default_flight_id)
    except (RequestException, KeyError, TypeError, URLError) as e:
        print(f"Ошибка при получении flight_id: {e}")
        return
    if not flight_id:
        print("Не удалось получить flight_id. Завершение работы.")
        return
    try:
        downloaded_images = fetch_spacex_images(flight_id)
    except OSError as e:
        print(f"Ошибка при скачивании изображений: {e}")
        return
    if downloaded_images:
        print(f"Успешно скачаны изображения: {downloaded_images}")
    else:
        print(f"Не удалось скачать изображения для запуска {flight_id}")


if __name__ == "__main__":
    main()
