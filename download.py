import io
import os
import zipfile

import requests
from github import Github

github_token = os.getenv("GITHUB_TOKEN")
repo_owner = "TVP-Support"
repo_name = "knowledge"
branch_name = "main"


def download_repo():
    g = Github(github_token)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    ref = f"refs/heads/{branch_name}"
    archive_format = "zipball"

    # Получаем ссылку на архив по заданному пути с помощью get_archive_link
    archive_url = repo.get_archive_link(archive_format, ref)

    # Загружаем содержимое архива в виде байтов
    archive_response = requests.get(archive_url)

    # Распаковываем содержимое архива в локальную директорию
    local_path = "src"
    os.makedirs(str(local_path), exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(archive_response.content)) as zip_file:
        zip_file.extractall(local_path)

    print("Репозиторий успешно скачан и распакован!")


if __name__ == "__main__":
    download_repo()
