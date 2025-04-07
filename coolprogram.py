import requests
import os


def download_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Изображение успешно скачано и сохранено в: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании изображения: {e}")
    except OSError as e:
        print(f"Произошла ошибка при сохранении изображения: {e}")
