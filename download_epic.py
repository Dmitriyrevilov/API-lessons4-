import os
import argparse
from dotenv import load_dotenv
from datetime import datetime
import requests
from coolprogram import download_image


def download_epic_images(num_images=5):
    directory = "epic_images"
    load_dotenv()
    API_NASA = os.getenv("API_NASA")
    try:
        os.makedirs(directory, exist_ok=True)
        url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={API_NASA}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            epic_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при скачивании JSON: {e}")
            return
        for image_info in epic_data[:num_images]:
            try:
                image_name = image_info["image"]
                image_date_str = image_info["date"]
                image_date = datetime.fromisoformat(
                    image_date_str.replace("Z", "+00:00")
                )
                year, month, day = (
                    image_date.year,
                    f"{image_date.month:02}",
                    f"{image_date.day:02}",
                )
                image_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={API_NASA}"
                filepath = os.path.join(directory, f"{image_name}.png")
                downloaded = download_image(image_url, filepath)
                if not downloaded:
                    print(f"Не удалось скачать изображение {image_url}")
            except Exception as e:
                print(
                    f"Ошибка при обработке EPIC image {image_info.get('image', 'неизвестного изображения')}: {e}"
                )
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скачивает EPIC изображения от NASA.")
    parser.add_argument(
        "--num_images",
        type=int,
        default=5,
        help="Количество изображений для скачивания (по умолчанию: 5)",
    )
    args = parser.parse_args()
    download_epic_images(args.num_images)
