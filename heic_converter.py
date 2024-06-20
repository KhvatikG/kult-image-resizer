import pillow_heif
from PIL import Image


def convert_heic_to_jpg(heic_path: str, jpg_path: str) -> None:
    """
    Конвертирует файл .HEIC находящийся по пути heic_path в jpg и сохраняет по пути jpg_path

    :param heic_path: Путь до файла .HEIC который необходимо конвертировать.
    :param jpg_path: Путь включающий имя файла для сохранения результата.
    """
    heif_file = pillow_heif.read_heif(heic_path)
    image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data)
    image.save(jpg_path, format="JPEG")
