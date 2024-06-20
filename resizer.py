from PIL import Image


def resize_image(source_path: str, save_path: str) -> None:
    """
    Принимает путь к файлу источнику и путь для сохранения.
    Изменяет размер изображения источника на 900 х 900
    :param source_path: Путь к изображению источнику
    :param save_path: Путь для сохранения файла
    :return:
    """
    try:
        with Image.open(source_path) as image:
            image.thumbnail((900, 900))
            image.save(save_path, format='JPEG')
            print(f"Изображение успешно изменено и сохранено по пути: {save_path}")
    except Exception as exc:
        print(f"Произошла ошибка при изменении размера изображения {source_path}: {exc}")
