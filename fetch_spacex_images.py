import requests
import os
import argparse
from dotenv import load_dotenv
from coolprogram import download_image


def get_flight_id():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Скачивает изображения с запуска SpaceX. Если ID не указан, скачивает последний запуск."
    )
    parser.add_argument("--flight_id", help="ID запуска SpaceX.")
    args = parser.parse_args()
    default_flight_id = os.getenv("FLIGHT_ID")
    FLIGHT_ID = args.flight_id or default_flight_id
    if not FLIGHT_ID:
        url_latest = "https://api.spacexdata.com/v5/launches/latest"
        try:
            response = requests.get(url_latest)
            response.raise_for_status()
            FLIGHT_ID = response.json()["id"]
        except Exception as e:
            print(f"Не удалось получить ID последнего запуска: {e}")
            exit()
    return FLIGHT_ID


def fetch_spacex_images(flight_id):
    try:
        url_launch = f"https://api.spacexdata.com/v5/launches/{flight_id}"
        response_launch = requests.get(url_launch)
        response_launch.raise_for_status()
        launch = response_launch.json()
        image_urls = launch["links"]["flickr"]["original"]
        if not image_urls:
            print(f"Нет изображений для запуска с ID: {flight_id}")
            return
        os.makedirs("images_spacex", exist_ok=True)
        for image_number, image_url in enumerate(image_urls):
            filename = f"spacex_{image_number}.jpeg"
            filepath = os.path.join("images_spacex", filename)
            downloaded = download_image(image_url, filepath)
            if not downloaded:
                print(f"Не удалось скачать изображение {image_url}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных о запуске: {e}")
    except (KeyError, TypeError) as e:
        print(f"Ошибка в структуре данных JSON: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    flight_id = get_flight_id()
    fetch_spacex_images(flight_id)
