import os
import argparse
from datetime import datetime
import requests
from urllib.error import URLError
from requests.exceptions import RequestException


def get_epic(nasa_api_key):
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": nasa_api_key}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def download_image_with_params(url, filepath, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(filepath, "wb") as f:
        f.write(response.content)
    return True


def download_epic_images(num_images=5, nasa_api_key=None):
    directory = "epic_images"
    if not nasa_api_key:
        print("Ошибка: Не передан API ключ NASA.")
        return None
    os.makedirs("epic_images", exist_ok=True)
    epic_entries = get_epic(nasa_api_key)
    downloaded_images = []
    for image_info in epic_entries[:num_images]:
        image_name = image_info["image"]
        image_date_str = image_info["date"]
        image_date = datetime.fromisoformat(image_date_str.replace("Z", "+00:00"))
        year, month, day = (
            image_date.year,
            f"{image_date.month:02}",
            f"{image_date.day:02}",
        )
        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
        filepath = os.path.join(directory, f"{image_name}.png")
        params = {"api_key": nasa_api_key}
        success = download_image_with_params(image_url, filepath, params)
        if success:
            downloaded_images.append(image_url)
        else:
            print(f"Не удалось скачать изображение {image_url}")
    return downloaded_images


def main():
    nasa_api_key = os.getenv("NASA_API_KEY")
    if not nasa_api_key:
        print("Ошибка: Не найден NASA_API_KEY в переменных окружения.")
        return
    parser = argparse.ArgumentParser(description="Скачивает EPIC изображения от NASA.")
    parser.add_argument(
        "--num_images",
        type=int,
        default=5,
        help="Количество изображений для скачивания (по умолчанию: 5)",
    )
    parser.add_argument(
        "--directory",
        default=os.getenv("EPIC_DIRECTORY", "epic_images"),
        help="Директория для сохранения изображений (по умолчанию: epic_images, или переменная окружения EPIC_DIRECTORY)",
    )
    args = parser.parse_args()
    try:
        downloaded_images = download_epic_images(args.num_images, nasa_api_key)
        if downloaded_images:
            print(f"Успешно скачаны изображения: {downloaded_images}")
        else:
            print("Не удалось скачать изображения EPIC.")
    except (RequestException, URLError, KeyError, OSError) as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
