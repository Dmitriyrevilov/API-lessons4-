import os
import argparse

from urllib.parse import urlparse
from os.path import basename
import requests
from coolprogram import download_image
from urllib.error import URLError
from requests.exceptions import RequestException


def get_apod_data(start_date, end_date, nasa_api_key):
    url_apod = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": nasa_api_key,
        "start_date": start_date,
        "end_date": end_date,
    }
    response = requests.get(url_apod, params=params)
    response.raise_for_status()
    return response.json()


def download_apod_images(start_date, end_date, api_nasa):
    os.makedirs("apod_images", exist_ok=True)
    apod = get_apod_data(start_date, end_date, api_nasa)
    if isinstance(apod, dict):
        apod = [apod]
    downloaded_images = []
    for apod in apod:
        if "url" in apod:
            image_url = apod["url"]
            parsed_url = urlparse(image_url)
            filename = basename(parsed_url.path)
            filepath = os.path.join("apod_images", filename)
            success = download_image(image_url, filepath)
            if success:
                downloaded_images.append(image_url)
            else:
                print(f"Не удалось скачать изображение {image_url}")
        else:
            print(
                f"Пропущено: Нет URL для APOD от {apod.get('date', 'неизвестной даты')}"
            )
    return downloaded_images


def main():
    nasa_api_key = os.getenv("NASA_API_KEY")
    if not nasa_api_key:
        print("Ошибка: Не найден NASA_API_KEY в переменных окружения.")
        return
    parser = argparse.ArgumentParser(
        description="Скачивает изображения APOD от NASA за указанный период."
    )
    parser.add_argument("start_date", help="Начальная дата (YYYY-MM-DD)")
    parser.add_argument("end_date", help="Конечная дата (YYYY-MM-DD)")
    args = parser.parse_args()
    try:
        downloaded_images = download_apod_images(
            args.start_date, args.end_date, nasa_api_key
        )
        if downloaded_images:
            print(f"Успешно скачаны изображения: {downloaded_images}")
        else:
            print("Не удалось скачать изображения APOD.")
    except (RequestException, URLError, OSError) as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
