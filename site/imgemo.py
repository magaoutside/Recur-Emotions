import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
from datetime import datetime

# Список меток эмоций, которые может распознавать модель
emotion_labels = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise', 'Neutral']

# Функция для записи логов в файл
def log_emotion(image_name, emotion, confidence):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Создаем папку logs, если она не существует
    
    log_file = os.path.join(log_dir, "imglog.txt")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Получаем текущее время
    log_entry = f"{image_name} - {current_time} - {emotion} - {confidence:.2f}%\n"
    
    with open(log_file, "a") as f:
        f.write(log_entry)  # Записываем лог в файл

# Функция для предсказания эмоции на изображении
def predict_emotion(frame, model, image_name):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        face = gray[y:y + h, x:x + w]
        face_resized = cv2.resize(face, (48, 48))
        face_normalized = face_resized / 255.0
        face_reshaped = np.expand_dims(face_normalized, axis=0)
        face_reshaped = np.expand_dims(face_reshaped, axis=-1)
        emotion_prediction = model.predict(face_reshaped)
        max_index = np.argmax(emotion_prediction[0])
        emotion = emotion_labels[max_index]
        confidence = np.max(emotion_prediction[0]) * 100
        
        # Логируем эмоцию и точность
        log_emotion(image_name, emotion, confidence)
        
        # Вывод эмоции и процента уверенности в консоль
        print(f"Эмоция: {emotion}, Уверенность: {confidence:.2f}%")

    return frame

# Функция для обработки изображения
def process_image(image_path):
    try:
        # Загрузка модели для распознавания эмоций
        model = tf.keras.models.load_model("model/model.h5")
        print("Модель успешно загружена.")
    except Exception as e:
        # Обработка ошибки загрузки модели
        print(f"Ошибка загрузки модели: {e}")
        return

    # Загрузка изображения
    frame = cv2.imread(image_path)
    if frame is None:
        # Обработка ошибки загрузки изображения
        print("Ошибка загрузки изображения.")
        return

    # Получаем название файла из пути
    image_name = os.path.basename(image_path)

    # Определение эмоции на изображении
    predict_emotion(frame, model, image_name)
    
    # Сообщение о завершении работы
    print("Работа завершена.")
    return

# Основной блок кода
if __name__ == "__main__":
    # Ввод пути к изображению
    image_path = input("Введите путь к изображению: ")
    
    # Преобразование пути в абсолютный
    image_path = os.path.abspath(image_path)

    # Проверка существования файла
    if not os.path.exists(image_path):
        print(f"Файл не найден: {image_path}")
    else:
        print(f"Файл найден: {image_path}")
        # Обработка изображения
        process_image(image_path)