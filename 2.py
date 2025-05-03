import requests
import json
from pathlib import Path

# 1. Получаем данные от NASA API
def fetch_nasa_apod():
    api_key = "AvCd8Ll7HbtTldQlV2LYPD7AtPlvPTY4s4mHhHJI"
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка при запросе: {e}")
        return None

# 2. Сохраняем в файл f.json
def save_to_file(data, filename="f.json"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Данные сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")

# 3. Читаем из файла
def load_from_file(filename="f.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None
    except Exception as e:
        print(f"Ошибка при чтении: {e}")
        return None

# Основной код
if __name__ == "__main__":
    # Вариант 1: Получить свежие данные и сохранить
    apod_data = fetch_nasa_apod()
    if apod_data:
        save_to_file(apod_data)
    
    # Вариант 2: Работа с сохранённым файлом
    saved_data = load_from_file()
    
    if saved_data:
        print("\n🌌 Данные из файла f.json:")
        print(f"Дата: {saved_data.get('date')}")
        print(f"Название: {saved_data.get('title')}")
        print(f"Описание: {saved_data.get('explanation')[:100]}...")  # Первые 100 символов
