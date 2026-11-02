"""Модуль обрабатывает консольную команду `vextract album`."""

import os

import click
import requests

from vextractor.utils import define_result_folder_path
from vextractor.vk.core import VK


@click.command
@click.help_option("-h", "--help")
@click.option("--login", envvar="VK_LOGIN", help="Fill vk login from console.")
@click.password_option(envvar="VK_PASSWORD", help="Fill vk password from console.")
@click.option("--limit", type=int, default=0, help="Limit of photos by one request.")
@click.argument("url", required=True)
def album(login: str, password: str, limit: int, url: str) -> None:
    """Extract photos from an album."""

    owner, album = VK.extract_album_parametrs_from_url(url)

    api = VK(login, password)
    img_list = api.get_list_of_album_images(owner, album)  # список изображений

    click.echo("A list of images has been generated.")

    # Collect all links of "maximum" size (w): https://vk.com/dev/objects/photo_sizes
    w_img_list = [
        img["url"]
        for item in img_list["items"]
        for img in item["sizes"]
        if img["type"] == "w"
    ]

    click.echo("A list of images has been collected.")

    if len(w_img_list) > 0:
        # Define result folder path by album id
        result_path = define_result_folder_path(album)

    with click.progressbar(
        length=len(w_img_list), label="Downloading Images"
    ) as progress_bar:
        for i, url in enumerate(w_img_list[: limit or len(w_img_list)]):
            response = requests.get(url)

            file_name = f"{i+1}.jpg"

            with click.open_file(
                os.path.join(result_path, file_name), "wb", encoding="utf-8"
            ) as f:
                f.write(response.content)

            progress_bar.update(1)

    click.echo(f"Загружено {len(w_img_list)} изображений в {result_path}")
