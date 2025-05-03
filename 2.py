import requests
import json

class TextAnalyzer:
    def __init__(self):
        self.text2data_url = "http://api.text2data.com/v3/analyze"
        self.numbersapi_url = "http://numbersapi.com/"
        self.text2data_key = "94B27606-BF53-415D-B690-A45D611DF7C9"  # Замените на свой ключ

    def analyze_text(self, text):
        """Анализирует текст с помощью text2data API"""
        payload = {
            'DocumentText': text,
            'IsTwitterContent': 'false',
            'PrivateKey': self.text2data_key,
            'Secret': '123',
            'RequestIdentifier': ''
        }

        try:
            response = requests.post(self.text2data_url, data=payload)
            response.raise_for_status()
            data = response.json()

            if data['Status'] != 1:
                return {"error": data['ErrorMessage']}

            analysis_result = {
                "sentiment": {
                    "polarity": data['DocSentimentPolarity'],
                    "result": data['DocSentimentResultString'],
                    "value": data['DocSentimentValue']
                },
                "magnitude": data['Magnitude'],
                "subjectivity": data['Subjectivity'],
                "core_sentences": [item['Text'] for item in data['CoreSentences']],
                "keywords": [
                    {
                        "text": item['Text'],
                        "type": item['KeywordType'],
                        "sentiment": {
                            "polarity": item['SentimentPolarity'],
                            "result": item['SentimentResult'],
                            "value": item['SentimentValue']
                        }
                    } for item in data['Keywords']
                ]
            }
            return analysis_result

        except requests.exceptions.RequestException as e:
            return {"error": f"Ошибка запроса: {str(e)}"}
        except (KeyError, json.JSONDecodeError) as e:
            return {"error": f"Ошибка обработки данных: {str(e)}"}

    def get_number_fact(self, number, fact_type):
        """Получает факт о числе через Numbers API"""
        try:
            response = requests.get(f"{self.numbersapi_url}/{number}/{fact_type}")
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            return f"Ошибка при получении факта: {str(e)}"

    def print_analysis(self, analysis):
        """Выводит результаты анализа в структурированном виде"""
        if "error" in analysis:
            print(f"Ошибка: {analysis['error']}")
            return

        print("\nРезультаты анализа текста:")
        print(f"Тональность: {analysis['sentiment']['polarity']}{analysis['sentiment']['result']} "
              f"(значение: {analysis['sentiment']['value']:+.2f})")
        print(f"Интенсивность: {analysis['magnitude']:.2f}")
        print(f"Субъективность: {analysis['subjectivity']}")

        print("\nОсновные предложения:")
        for i, sentence in enumerate(analysis['core_sentences'], 1):
            print(f"{i}. {sentence}")

        print("\nКлючевые слова:")
        for keyword in analysis['keywords']:
            print(f"- {keyword['text']} ({keyword['type']}): "
                  f"{keyword['sentiment']['polarity']}{keyword['sentiment']['result']} "
                  f"({keyword['sentiment']['value']:+.2f})")

def main():
    analyzer = TextAnalyzer()
    
    print("Программа для анализа текста и получения фактов о числах")
    print("Выберите действие:")
    print("1 - Интересные факты о числах")
    print("2 - Математические факты о числах")
    print("3 - Анализ произвольного текста")
    print("0 - Выход")

    while True:
        choice = input("\nВведите номер действия: ").strip()

        if choice == '0':
            print("Программа завершена.")
            break

        elif choice in ('1', '2'):
            fact_type = 'trivia' if choice == '1' else 'math'
            number = input("Введите число: ").strip()
            
            if not number.isdigit():
                print("Ошибка: введите корректное число")
                continue
                
            fact = analyzer.get_number_fact(number, fact_type)
            print(f"\nФакт о числе {number}: {fact}")
            
            analysis = analyzer.analyze_text(fact)
            analyzer.print_analysis(analysis)

        elif choice == '3':
            text = input("Введите текст для анализа: ").strip()
            if not text:
                print("Ошибка: текст не может быть пустым")
                continue
                
            analysis = analyzer.analyze_text(text)
            analyzer.print_analysis(analysis)

        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()
