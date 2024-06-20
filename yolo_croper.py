import cv2
import numpy as np
from PIL import Image
from config import settings


def load_yolo_model(cfg_path, weights_path, names_path):
    net = cv2.dnn.readNet(weights_path, cfg_path)
    with open(names_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    return net, classes


def detect_burger(image, net, output_layers, classes, target_class="sandwich"):
    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] == target_class:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    if len(indices) > 0:
        burger_box = boxes[indices[0]]
        return burger_box
    else:
        return None


def crop_to_square_by_height(image_path, output_path):
    # Загрузить и инициализировать модель YOLO
    net, classes = load_yolo_model(settings.yolo_cfg, settings.yolo_weights, settings.yolo_names)

    # Получение списка выходных слоев
    layer_names = net.getLayerNames()

    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except Exception as e:
        raise IndexError(f"Ошибка при получении выходных слоев модели: {e}")

    # Загрузить изображение
    image = cv2.imread(image_path)

    # Проверка на успешную загрузку изображения
    if image is None:
        raise FileNotFoundError(f"Изображение по пути {image_path} не найдено или не удалось загрузить.")

    # Получить текущие ширину и высоту изображения
    height, width, _ = image.shape

    # Пытаемся обнаружить бургер
    burger_box = detect_burger(image, net, output_layers, classes)

    if burger_box:
        x, y, w, h = burger_box
        centerY = y + h // 2
    else:
        centerY = height // 2  # Если бургер не найден, берем центр изображения

    # Обрезать изображение по высоте так, чтобы бургер был в центре
    start_y = max(centerY - width // 2, 0)
    end_y = min(centerY + width // 2, height)

    cropped_image = image[start_y:end_y, :]

    # Если обрезанное изображение меньше по высоте, чем ширина, добавить черные полосы
    if (end_y - start_y) < width:
        padding = (width - (end_y - start_y)) // 2
        cropped_image = cv2.copyMakeBorder(cropped_image, padding, padding, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))

    # Сохранить изображение
    cropped_image_pil = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    cropped_image_pil.save(output_path)
