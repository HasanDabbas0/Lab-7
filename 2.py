import requests
from pprint import pprint

def get_nasa_apod(api_key="AvCd8Ll7HbtTldQlV2LYPD7AtPlvPTY4s4mHhHJI"):
    """Получаем Astronomy Picture of the Day от NASA с вашим ключом"""
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        return {"error": f"HTTP ошибка: {errh}"}
    except requests.exceptions.ConnectionError as errc:
        return {"error": f"Ошибка подключения: {errc}"}
    except requests.exceptions.Timeout as errt:
        return {"error": f"Таймаут: {errt}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Ошибка запроса: {err}"}

def display_apod(data):
    """Красивый вывод данных APOD"""
    print("\n🌌 NASA Astronomy Picture of the Day")
    print("===================================")
    
    if 'error' in data:
        print(f"❌ Ошибка: {data['error']}")
        return
    
    print(f"📅 Дата: {data.get('date', 'неизвестна')}")
    print(f"🖼️ Название: {data.get('title', 'без названия')}")
    print(f"📷 Тип контента: {data.get('media_type', 'неизвестен')}")
    
    if data.get('media_type') == 'image':
        print(f"\n🔗 Ссылки:")
        print(f"HD: {data.get('hdurl', 'нет')}")
        print(f"Обычное: {data.get('url', 'нет')}")
    
    print("\n📝 Описание:")
    print(data.get('explanation', 'Описание отсутствует'))
    
    if 'copyright' in data:
        print(f"\n© Автор: {data['copyright']}")

def main():
    print("Загружаем данные от NASA API...")
    apod_data = get_nasa_apod()
    display_apod(apod_data)
    
    # Дополнительная проверка для видео
    if 'media_type' in apod_data and apod_data['media_type'] == 'video':
        print("\n🎥 Видео доступно по ссылке:", apod_data.get('url'))

if __name__ == "__main__":
    main()
