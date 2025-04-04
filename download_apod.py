import os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse
from os.path import basename
import requests
from coolprogram import download_image


def download_apod_images(start_date, end_date):
    load_dotenv()
    api_nasa = os.getenv("API_NASA")
    try:
        os.makedirs("apod_images", exist_ok=True)
        url_apod = "https://api.nasa.gov/planetary/apod"
        params = {
            "api_key": api_nasa,
            "start_date": start_date,
            "end_date": end_date,
        }
        try:
            response = requests.get(url_apod, params=params)
            response.raise_for_status()
            apod_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при скачивании JSON: {e}")
            return
        if isinstance(apod_data, dict):
            apod_data = [apod_data]
        for apod in apod_data:
            try:
                if "url" in apod:
                    image_url = apod["url"]
                    parsed_url = urlparse(image_url)
                    filename = basename(parsed_url.path)
                    filepath = os.path.join("apod_images", filename)
                    downloaded = download_image(image_url, filepath)
                    if not downloaded:
                        print(f"Не удалось скачать изображение {image_url}")
                else:
                    print(
                        f"Пропущено: Нет URL для APOD от {apod.get('date', 'неизвестной даты')}"
                    )

            except Exception as e:
                print(
                    f"Ошибка при обработке APOD от {apod.get('date', 'неизвестной даты')}: {e}"
                )
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Скачивает изображения APOD от NASA за указанный период."
    )
    parser.add_argument("start_date", help="Начальная дата (YYYY-MM-DD)")
    parser.add_argument("end_date", help="Конечная дата (YYYY-MM-DD)")
    args = parser.parse_args()
    download_apod_images(args.start_date, args.end_date)

# Как исправить ошибку:

# Вам нужно указать начальную и конечную даты при запуске скрипта. Например:

# python download_apod.py 2023-12-01 2023-12-31
