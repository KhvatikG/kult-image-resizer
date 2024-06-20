from config import settings
from collector import get_files
from heic_converter import convert_heic_to_jpg
from yolo_croper import crop_to_square_by_height
from resizer import resize_image
from tmp_remover import remove_files


# Получаем список файлов в папке
input_file_list = get_files(settings.input_folder_path)
jpg_file_list = []
cropped_file_list = []

# Конвертим файлы в jpeg
for heic_file in input_file_list:
    jpg_name = settings.get_jpg_path(input_file_path=heic_file)
    heic_path = settings.input_folder_path + '/' + heic_file
    try:
        convert_heic_to_jpg(heic_path=heic_path, jpg_path=jpg_name)
        jpg_file_list.append(jpg_name)
    except Exception as exc:
        print(f'Ошибка конвертации: {exc}')

# Обрезаем файлы jpg
for jpg_file in jpg_file_list:
    try:
        result_file_path = settings.get_result_path(jpg_file)
        crop_to_square_by_height(image_path=jpg_file, output_path=result_file_path)
        cropped_file_list.append(result_file_path)
    except Exception as exc:
        print(f'Не удалось обрезать файл {jpg_file}: {exc}')


# Изменяем размер файлов
for cropped_file in cropped_file_list:
    resized_file_path = settings.get_resized_result_path(cropped_file)
    resize_image(source_path=cropped_file, save_path=resized_file_path)

# Удаляем временные jpg файлы
remove_files(settings.tmp_jpg_folder_path)
remove_files(settings.output_folder_path)
# remove_files(settings.input_folder_path)
