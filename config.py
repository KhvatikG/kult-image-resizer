from pydantic import BaseModel


class Settings(BaseModel):

    # Пути к папкам
    input_folder_path: str = 'input_images'
    output_folder_path: str = 'output_images'
    tmp_jpg_folder_path: str = 'tmp_jpg'
    resize_result_folder_path: str = 'resized_result'

    # Префикс для имени результатирующего изображения
    out_name_prefix: str = 'result'

    # Пути к YOLO файлам
    yolo_cfg: str = 'models/yolov3.cfg'
    yolo_weights: str = 'models/yolov3.weights'
    yolo_names: str = 'models/coco.names'

    def get_jpg_path(self, input_file_path: str) -> str:
        """
        Принимает путь к HEIC файлу, возвращает путь для сохранения jpg файла(включая имя)

        :param input_file_path: Путь к файлу
        :return: Путь для сохранения файла включая имя
        """

        return f"{self.tmp_jpg_folder_path}/{input_file_path.split('/')[-1].replace('.HEIC', '.jpg')}"

    def get_result_path(self, jpg_file_path: str) -> str:
        """
        Принимает путь к jpg файлу до обрезки, возвращает путь для сохранения jpg файла(включая имя) после обрезки

        :param jpg_file_path: Путь к jpg файлу до обрезки
        :return: Путь для сохранения обрезанного jpg файла включая имя
        """

        return f"{self.output_folder_path}/{jpg_file_path.split('/')[-1]}"

    def get_resized_result_path(self, jpg_file_path: str) -> str:
        """
        Принимает путь к jpg файлу изменения размера, возвращает путь для сохранения jpg файла(включая имя) после

        :param jpg_file_path: Путь к jpg файлу до изменения размера
        :return: Путь для сохранения измененного jpg файла включая имя
        """

        return f"{self.resize_result_folder_path}/{jpg_file_path.split('/')[-1]}"


settings = Settings()
