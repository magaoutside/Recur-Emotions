import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
from datetime import datetime

# Список эмоций, которые будет распознавать модель
emotion_labels = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise', 'Neutral']

# Функция для записи логов в файл
def log_emotion(emotion, confidence):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Создаем папку logs, если она не существует
    
    log_file = os.path.join(log_dir, "cameralog.txt")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Получаем текущее время
    log_entry = f"{current_time} - {emotion} - {confidence:.2f}%\n"
    
    with open(log_file, "a") as f:
        f.write(log_entry)  # Записываем лог в файл

# Функция для предсказания эмоции на изображении
def predict_emotion(frame, model):
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
        log_emotion(emotion, confidence)
        
        # Добавление текста с эмоцией на изображение
        cv2.putText(frame, f"{emotion} {confidence:.2f}%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return frame

# Функция для включения камеры и отображения эмоций в реальном времени
def start_camera():
    try:
        # Загрузка модели для распознавания эмоций
        model = tf.keras.models.load_model("model/model.h5")
        print("Модель успешно загружена.")
    except Exception as e:
        # Обработка ошибки загрузки модели
        print(f"Ошибка загрузки модели: {e}")
        return

    # Инициализация видеозахвата с камеры
    cap = cv2.VideoCapture(0)

    # Установка параметров камеры
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Ширина кадра
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Высота кадра
    cap.set(cv2.CAP_PROP_FPS, 60)  # Частота кадров

    # Проверка применённых настроек камеры
    print("Установленные параметры камеры:")
    print("Ширина кадра:", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("Высота кадра:", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("FPS камеры:", cap.get(cv2.CAP_PROP_FPS))

    # Проверка, открыта ли камера
    if not cap.isOpened():
        print("Ошибка: камера недоступна.")
        return

    # Сообщение о успешном подключении камеры
    print("Камера подключена. Нажмите 'q' для выхода.")
    
    try:
        # Основной цикл для захвата и обработки кадров
        while True:
            # Захват кадра с камеры
            ret, frame = cap.read()
            
            # Проверка успешности захвата кадра
            if not ret:
                print("Ошибка захвата кадра. Проверьте подключение камеры.")
                break

            # Предсказание эмоции на текущем кадре
            frame_with_emotions = predict_emotion(frame, model)
            
            # Отображение изображения с наложенными эмоциями
            cv2.imshow('Emotion Recognition', frame_with_emotions)

            # Выход из цикла по нажатию клавиши 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Выход.")
                break
    except Exception as e:
        # Обработка ошибок во время работы камеры
        print(f"Ошибка во время работы камеры: {e}")
    finally:
        # Освобождение ресурсов камеры и закрытие окон
        cap.release()
        cv2.destroyAllWindows()