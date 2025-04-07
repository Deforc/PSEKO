import os

def extract_filename(text):
    """
    Извлекает название файла из первой строки текста.
    """
    # Разделяем текст на строки
    lines = text.splitlines()

    # Проверяем, что текст не пустой и первая строка существует
    if not lines:
        raise ValueError("Text is empty or does not contain any lines.")

    # Извлекаем первую строку и удаляем лишние пробелы
    first_line = lines[0].strip()

    # Проверяем, что строка заканчивается на .yaml
    # if not first_line.endswith('.yaml'):
    #     raise ValueError(f"The first line '{first_line}' is not a valid YAML file name.")

    return first_line

def get_yaml_file_path(chosen_file):
    yaml_dir = os.path.join(os.getcwd(), 'yaml')

    # Полный путь до файла
    file_path = os.path.join(yaml_dir, chosen_file)

    # Проверка существования файла
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{chosen_file}' not found in directory '{yaml_dir}'.")

    return file_path