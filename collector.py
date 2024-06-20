import os


def get_files(folder_path):
    heic_files_ = []

    files = os.listdir(folder_path)

    for file in files:
        if file.lower().endswith('.heic'):
            heic_files_.append(file)
        else:
            print(f"Невозможно обработать файл {file}. Пока не могу работать с данным форматом.")

    return heic_files_
