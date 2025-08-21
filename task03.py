import json
import sys
from itertools import product
from CLI_color import *


def generate_versions(template):
    parts = template.split(".")
    wildcard_indices = [i for i, part in enumerate(parts) if part == "*"]

    if not wildcard_indices:
        return [template]

    # Генерируем все возможные комбинации для звездочек
    replacements = []
    for _ in wildcard_indices:
        replacements.append(
            ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        )  # Можно изменить

    versions = []
    for combo in product(*replacements):
        temp_parts = parts.copy()
        for i, idx in enumerate(wildcard_indices):
            temp_parts[idx] = combo[i]
        versions.append(".".join(temp_parts))

    # Возвращаем 2 уникальных варианта
    return sorted(list(set(versions)))[:2]


def version_to_tuple(version):
    return tuple(map(int, version.split(".")))


def main():
    if len(sys.argv) != 3:
        print(
            f"{color_grey}Usage: python3 <script_name> <version> <config_file>{color_end}"
        )
        sys.exit(1)

    input_version = sys.argv[1]
    config_file = sys.argv[2]

    try:
        with open(config_file, "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"{color_red}Error reading config file: {e}{color_end}")
        sys.exit(1)

    all_versions = []

    for template in config.values():
        versions = generate_versions(template)
        all_versions.extend(versions)

    # Удаляем дубликаты и сортируем
    unique_versions = sorted(list(set(all_versions)), key=version_to_tuple)

    print(f"{color_green}All generated versions (sorted):{color_end}")
    for version in unique_versions:
        print(version)

    print(f"\n{color_green}Versions older than", input_version + f":{color_end}")
    input_tuple = version_to_tuple(input_version)
    older_versions = [v for v in unique_versions if version_to_tuple(v) < input_tuple]

    for version in older_versions:
        print(version)


if __name__ == "__main__":
    main()
