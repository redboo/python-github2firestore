import glob
import os

from firebase_admin import credentials, initialize_app, storage

# Инициализация приложения Firebase с использованием файла с учетными данными
cred = credentials.Certificate("credentials.json")
initialize_app(cred, {"storageBucket": "hidden-bruin-305018.appspot.com"})

# Путь к папке с ресурсами
root_path = "src"
target_folder = "assets"
assets_path = glob.glob(os.path.join(root_path, "**", target_folder), recursive=True)[0]

if not assets_path:
    print(f"Директория '{target_folder}' не найдена в '{root_path}'")
else:
    print(f"Путь к '{target_folder}': {assets_path}")

    # Получаем список файлов в папке
    files = os.listdir(assets_path)

    # Создаем объект бакета и получаем ссылку на него
    bucket = storage.bucket()

    # Загружаем каждый файл в Firebase Storage
    for file_name in files:
        # Формируем путь к файлу
        file_path = os.path.join(assets_path, file_name)

        # Создаем объект blob и загружаем файл
        blob = bucket.blob(f"assets/{file_name}")
        blob.upload_from_filename(file_path)

        # Делаем файл публичным
        blob.make_public()

        # Выводим ссылку на файл
        print(f"Ссылка на файл '{file_name}': {blob.public_url}")
