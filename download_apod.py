import os
import argparse

from urllib.parse import urlparse
from os.path import basename
import requests
from coolprogram import download_image
from urllib.error import URLError
from requests.exceptions import RequestException


def get_apod_data(start_date, end_date, NASA_API_KEY):
    url_apod = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": NASA_API_KEY,
        "start_date": start_date,
        "end_date": end_date,
    }
    response = requests.get(url_apod, params=params)
    response.raise_for_status()
    return response.json()


def download_apod_images(start_date, end_date, NASA_API_KEY, directory):
    os.makedirs(directory, exist_ok=True)
    try:
        apod_entries = download_apod_images(start_date, end_date, NASA_API_KEY)
    except RequestException as e:
        print(f"Ошибка при получении данных APOD: {e}")
        return []

    if isinstance(apod_entries, dict):
        apod_entries = [apod_entries]

    downloaded_images = []
    for apod_entry in apod_entries:
        if apod_entry.get("media_type") == "image":
            image_url = apod_entry.get("url") or apod_entry.get("hdurl")
            if image_url:
                parsed_url = urlparse(image_url)
                filename = basename(parsed_url.path)
                filepath = os.path.join(directory, filename)
                success = download_image(image_url, filepath)
                if success:
                    downloaded_images.append(image_url)
                else:
                    print(f"Не удалось скачать изображение {image_url}")
            else:
                print(
                    f"Пропущено: Нет URL или HDURL для APOD от {apod_entry.get('date', 'неизвестной даты')}"
                )
        else:
            print(
                f"Пропущено: APOD от {apod_entry.get('date', 'неизвестной даты')} имеет тип {apod_entry.get('media_type')}, требуется 'image'."
            )
    return downloaded_images


def main():
    NASA_API_KEY = os.getenv("NASA_API_KEY")
    if not NASA_API_KEY:
        print("Ошибка: Не найден NASA_API_KEY в переменных окружения.")
        return
    parser = argparse.ArgumentParser(
        description="Скачивает изображения APOD от NASA за указанный период."
    )
    parser.add_argument("start_date", help="Начальная дата (YYYY-MM-DD)")
    parser.add_argument("end_date", help="Конечная дата (YYYY-MM-DD)")
    parser.add_argument(
        "--directory",
        default=os.getenv("APOD_DIRECTORY", "apod_images"),
        help="Директория для сохранения изображений (по умолчанию: apod_images, или переменная окружения APOD_DIRECTORY)",
    )
    args = parser.parse_args()
    try:
        downloaded_images = download_apod_images(
            args.start_date, args.end_date, NASA_API_KEY
        )
        if downloaded_images:
            print(f"Успешно скачаны изображения: {downloaded_images}")
        else:
            print("Не удалось скачать изображения APOD.")
    except (RequestException, URLError, OSError) as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
