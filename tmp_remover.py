import os


def remove_files(dir_path: str) -> None:
    """
    Удаляет все файлы в указанной директории

    :param dir_path: Путь к директории для удаления файлов
    """

    files = os.listdir(dir_path)

    for file in files:
        file_path = os.path.join(dir_path, file)

        if os.path.isfile(file_path):
            os.remove(file_path)
