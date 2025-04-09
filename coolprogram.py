import requests
import os


def download_image(image_url, save_path):
    response = requests.get(image_url)
    response.raise_for_status()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(response.content)
    return True
