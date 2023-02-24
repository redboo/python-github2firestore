import os

import firebase_admin
from firebase_admin import credentials, firestore

# Инициализация Firestore
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Поиск пути к директории с файлами для загрузки
root_path = "src"
target_folder = "db"
path = next(
    (os.path.join(dirpath, target_folder) for dirpath, dirnames, _ in os.walk(root_path) if target_folder in dirnames),
    None,
)

if not path:
    print(f"Директория '{target_folder}' не найдена в '{root_path}'")
else:
    print(f"Путь к '{target_folder}': {path}")

    # Создание объекта batch и добавление операций записи в него
    batch = db.batch()
    batch_size = 0

    for filename in os.listdir(path):
        with open(os.path.join(path, filename), "r") as f:
            content = f.read()
            doc_ref = db.collection("files").document(filename.rstrip(".md"))
            batch.set(doc_ref, {"content": content})
            batch_size += 1

            if batch_size == 500:  # Лимит размера батча - 500 операций записи
                batch.commit()
                print(f"{batch_size} файлов загружены в Firestore!")
                batch = db.batch()
                batch_size = 0

    # Выполнение оставшихся операций записи данных
    if batch_size > 0:
        batch.commit()
        print(f"{batch_size} файлов загружены в Firestore!")

    print("Файлы загружены в Firestore!")
