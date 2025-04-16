import requests
import os


def download_image(image_url, path):
    response = requests.get(image_url)
    response.raise_for_status()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(response.content)
    return True
