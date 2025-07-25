import os
import json
import shutil
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

color_red = "\033[31m"
color_green = "\033[32m"
color_ellow = "\033[33m"
color_grey = "\033[90m"
color_end = "\033[0m"


def log_message(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{color_grey}{current_time}{color_end} {message}")


def clone_repository(repo_url, temp_dir):
    log_message(f"{color_ellow}Клонирование репозитория {repo_url}...{color_end}")
    try:
        subprocess.run(["git", "clone", repo_url, temp_dir], check=True)
        log_message(f"{color_green}Репозиторий успешно клонирован\033[0m{color_end}")
        return True
    except subprocess.CalledProcessError as e:
        log_message(f"{color_red}Ошибка при клонировании репозитория: {e}{color_end}")
        return False


def clean_directory(root_dir, keep_dir):
    log_message(
        f"{color_ellow}Очистка директории{color_end} {root_dir} {color_ellow}, сохранение только{color_end} {keep_dir}"
    )
    try:
        keep_path = Path(root_dir) / keep_dir
        if not keep_path.exists():
            log_message(
                f"{color_red}Ошибка: директория {keep_dir} не существует в репозитории{color_end}"
            )
            return False

        for item in os.listdir(root_dir):
            item_path = Path(root_dir) / item
            if item_path != keep_path and item_path.is_dir():
                shutil.rmtree(item_path)
                log_message(f"{color_ellow}Удалена директория:{color_end} {item}")

        log_message(f"{color_green}Очистка завершена{color_end}")
        return True
    except Exception as e:
        log_message(f"{color_red}Ошибка при очистке директории: {e}{color_end}")
        return False


def create_version_file(src_dir, version):
    log_message(f"{color_ellow}Создание version.json в {src_dir}...{color_end}")
    try:
        # Получаем список файлов с нужными расширениями
        extensions = (".py", ".js", ".sh")
        files = []
        for ext in extensions:
            files.extend([f.name for f in Path(src_dir).rglob(f"*{ext}")])

        # Получаем имя директории для поля "name"
        dir_name = Path(src_dir).name

        version_data = {"name": dir_name, "version": version, "files": files}

        version_file = Path(src_dir) / "version.json"
        with open(version_file, "w") as f:
            json.dump(version_data, f, indent=4)

        log_message(f"{color_green}Файл version.json создан: {version_data}{color_end}")
        return True
    except Exception as e:
        log_message(f"{color_red}Ошибка при создании version.json: {e}{color_end}")
        return False


def create_archive(src_dir):
    log_message(f"{color_ellow}Создание архива из {src_dir}...{color_end}")
    try:
        dir_name = Path(src_dir).name
        current_date = datetime.now().strftime("%d%m%Y")
        archive_name = f"{dir_name}{current_date}.zip"

        shutil.make_archive(dir_name + current_date, "zip", src_dir)
        log_message(f"{color_green}Архив создан: {archive_name}{color_end}")
        return archive_name
    except Exception as e:
        log_message(f"{color_red}Ошибка при создании архива: {e}{color_end}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Универсальный сборочный скрипт")
    parser.add_argument("repo_url", help="URL репозитория")
    parser.add_argument("src_path", help="Относительный путь до исходного кода")
    parser.add_argument("version", help="Версия продукта")

    args = parser.parse_args()

    log_message(f"{color_ellow}Начало работы скрипта{color_end}")

    # Создаем временную директорию для клонирования
    temp_dir = "temp_repo"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    # Клонируем репозиторий
    if not clone_repository(args.repo_url, temp_dir):
        return

    # Очищаем директорию
    if not clean_directory(temp_dir, "src"):
        shutil.rmtree(temp_dir)
        return

    # Создаем version.json
    src_dir = os.path.join(temp_dir, args.src_path)
    if not create_version_file(src_dir, args.version):
        shutil.rmtree(temp_dir)
        return

    # Создаем архив
    archive_name = create_archive(src_dir)
    if not archive_name:
        shutil.rmtree(temp_dir)
        return

    # Удаляем временную директорию
    shutil.rmtree(temp_dir)

    log_message(
        f"{color_green}Скрипт завершил работу. Создан архив:{color_end} {archive_name}"
    )


if __name__ == "__main__":
    main()
