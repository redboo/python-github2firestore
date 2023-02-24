import os

from firebase_admin import credentials, initialize_app, storage

# Инициализация приложения Firebase с использованием файла с учетными данными
cred = credentials.Certificate("credentials.json")
initialize_app(cred, {"storageBucket": "hidden-bruin-305018.appspot.com"})

# Поиск пути к директории с файлами для загрузки
root_path = "src"
target_folder = "assets"
folder_path = next(
    (os.path.join(dirpath, target_folder) for dirpath, dirnames, _ in os.walk(root_path) if target_folder in dirnames),
    None,
)

if not folder_path:
    print(f"Директория '{target_folder}' не найдена в '{root_path}'")
else:
    print(f"Путь к '{target_folder}': {folder_path}")

    # Получаем список файлов в папке
    files = os.listdir(folder_path)

    # Создаем объект бакета и получаем ссылку на него
    bucket = storage.bucket()

    # Загружаем каждый файл в Firebase Storage
    for file_name in files:
        # Формируем путь к файлу
        file_path = os.path.join(folder_path, file_name)

        # Создаем объект blob и загружаем файл
        blob = bucket.blob(f"assets/{file_name}")
        blob.upload_from_filename(file_path)

        # Если нужно, делаем файл публичным
        blob.make_public()

        # Выводим ссылку на файл
        print(f"Ссылка на файл '{file_name}': {blob.public_url}")
