import requests
import os
import argparse
from coolprogram import download_image
from urllib.error import URLError
from requests.exceptions import RequestException


def get_flight_id(flight_id_arg=None, default_flight_id=None):
    flight_id = flight_id_arg or default_flight_id
    if not flight_id:
        url_latest = "https://api.spacexdata.com/v5/launches/latest"
        response = requests.get(url_latest)
        response.raise_for_status()
        flight_id = response.json()["id"]
    return flight_id


def fetch_spacex_images(flight_id):
    url_launch = f"https://api.spacexdata.com/v5/launches/{flight_id}"
    response_launch = requests.get(url_launch)
    response_launch.raise_for_status()
    launch = response_launch.json()
    image_urls = launch["links"]["flickr"]["original"]
    if not image_urls:
        print(f"Нет изображений для запуска с ID: {flight_id}")
        return []
    os.makedirs("images_spacex", exist_ok=True)
    downloaded_images = []
    for image_number, image_url in enumerate(image_urls):
        filename = f"spacex_{image_number}.jpeg"
        filepath = os.path.join("images_spacex", filename)
        success = download_image(image_url, filepath)
        if success:
            downloaded_images.append(image_url)
        else:
            print(f"Не удалось скачать изображение {image_url}")
    return downloaded_images


def main():
    parser = argparse.ArgumentParser(
        description="Скачивает изображения с запуска SpaceX. Если ID не указан, скачивает последний запуск."
    )
    parser.add_argument("--flight_id", help="ID запуска SpaceX.")
    args = parser.parse_args()
    default_flight_id = os.getenv("SPACEX_FLIGHT_ID")
    try:
        flight_id = get_flight_id(args.flight_id, default_flight_id)

        if flight_id:
            downloaded_images = fetch_spacex_images(flight_id)
            if downloaded_images:
                print(f"Успешно скачаны изображения: {downloaded_images}")
            else:
                print(f"Не удалось скачать изображения для запуска {flight_id}")
        else:
            print("Не удалось получить flight_id. Завершение работы.")
    except (RequestException, KeyError, TypeError, OSError, URLError) as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
