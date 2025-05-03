import requests
import random

# Базовый URL API Почты России
url = "https://www.pochta.ru/tracking"
print("Подключаемся к API Почты России...\n")

# Параметры для запроса
params = {
    'p_p_id': 'trackingPortlet_WAR_trackingportlet',
    'p_p_lifecycle': '2',
    'p_p_state': 'normal',
    'p_p_mode': 'view',
    'p_p_resource_id': 'tracking.get-by-barcode',
    'p_p_cacheability': 'cacheLevelPage'
}

# 1. Случайное отправление (пример трек-номера)
print("1. Случайное почтовое отправление:")
track_codes = ['RA', 'RB', 'CN', 'UA', 'LM']
random_track = f"{random.choice(track_codes)}{random.randint(100000000, 999999999)}RU"
params['_trackingPortlet_WAR_trackingportlet_barcode'] = random_track
response = requests.get(url, params=params)
print(f"Трек-номер: {random_track}")
print(response.json())
print()

# 2. Поиск по конкретному трек-номеру
print("2. Поиск по трек-номеру (пример):")
track_number = "RA123456789RU"  # Замените на реальный трек-номер
params['_trackingPortlet_WAR_trackingportlet_barcode'] = track_number
response = requests.get(url, params=params)
print(f"Трек-номер: {track_number}")
print(response.json())
print()

# 3. Получение истории отправления
print("3. История отправления:")
if 'trackingItem' in response.json():
    history = response.json()['trackingItem']['trackingHistoryItemList']
    for event in history:
        print(f"{event['date']} - {event['humanStatus']} ({event['address']['name']})")
else:
    print("Нет данных об отправлении")
print()

# 4. Проверка типа отправления
print("4. Тип отправления:")
if 'trackingItem' in response.json():
    mail_type = response.json()['trackingItem']['mailType']
    print(f"Тип: {mail_type}")
else:
    print("Тип отправления неизвестен")
