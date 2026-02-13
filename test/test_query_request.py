import pytest
import numpy as np
from query_request import Query


class TestTh:
    @pytest.fixture
    def query(self):
        return Query()

    def test_th(self, query):
        tests = [
            ("шустрик привет", "greeting"),
            ("шустрик здравствуй", "greeting"),
            ("шустрик добрый день", "greeting"),
            ("шустрик доброе утро", "greeting"),
            ("шустрик добрый вечер", "greeting"),
            ("шустрик приветик", "greeting"),
            ("шустрик салют", "greeting"),
            ("шустрик рад тебя видеть", "greeting"),
            ("шустрик сколько лет сколько зим", "greeting"),

            # farewell
            ("шустрик пока", "farewell"),
            ("шустрик пока пока", "farewell"),
            ("шустрик до свидания", "farewell"),
            ("шустрик до встречи", "farewell"),
            ("шустрик увидимся", "farewell"),
            ("шустрик всего доброго", "farewell"),
            ("шустрик спокойной ночи", "farewell"),
            ("шустрик сладких снов", "farewell"),

            # time
            ("шустрик который час", "time"),
            ("шустрик сколько сейчас времени", "time"),
            ("шустрик подскажи время", "time"),
            ("шустрик скажи точное время", "time"),
            ("шустрик время и дата", "time"),
            ("шустрик сколько времени в москве", "time"),
            ("шустрик сколько щас времени", "time"),

            # weather
            ("шустрик какая погода", "weather"),
            ("шустрик погода сегодня", "weather"),
            ("шустрик погода сейчас", "weather"),
            ("шустрик сколько градусов на улице", "weather"),
            ("шустрик какая температура на улице", "weather"),
            ("шустрик прогноз погоды на сегодня", "weather"),
            ("шустрик погода на завтра", "weather"),
            ("шустрик погода на неделю", "weather"),

            # open_program
            ("шустрик открой браузер", "open_program"),
            ("шустрик открой калькулятор", "open_program"),
            ("шустрик открой телеграм", "open_program"),
            ("шустрик запусти браузер", "open_program"),
            ("шустрик включи музыку", "open_program"),
            ("шустрик вруби ютуб", "open_program"),

            # wikipedia_search
            ("шустрик найди информацию о нейросетях", "wikipedia_search"),
            ("шустрик загугли что такое питон", "wikipedia_search"),
            ("шустрик поищи в интернете новости про технологии", "wikipedia_search"),
            ("шустрик найди в гугле курс доллара", "wikipedia_search"),
            ("шустрик поиск в википедии алан тьюринг", "wikipedia_search"),
            ("шустрик найди картинки котов", "wikipedia_search"),
            ("шустрик найди видео про космос", "wikipedia_search"),
        ]

        rapids = np.arange(0, 1.01, 0.01)
        best_accuracy = 0
        best_rapid = 0
        best_results = {}


        for rapid in rapids:
            correct = 0
            result = {}
            total = len(tests)

            for request, expected in tests:
                actual = query.get_intent(request, rapid)
                is_correct = actual == expected

                if is_correct:
                    correct += 1

                result[request] = {
                    'expected': expected,
                    'actual': actual,
                    'correct': is_correct
                }

            accuracy = correct / total

            if rapid % 0.1 == 0:
                print(f"Коэффициент: {rapid:.2f}, Точность: {accuracy:.2%}")

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_rapid = rapid
                best_results = result

        with open('best_rapid_results.txt', 'w', encoding='utf-8') as f:
            f.write(f"Лучший коэффициент: {best_rapid:.3f}\n")
            f.write(f"Точность: {best_accuracy:.2%}\n")
            f.write(f"Количество правильных: {int(best_accuracy * total)}/{total}\n")
            f.write(f"Количество неправильных: {total - int(best_accuracy * total)}/{total}\n\n")


            categories = {}
            for request, result in best_results.items():
                category = result['expected']
                if category not in categories:
                    categories[category] = []
                categories[category].append((request, result))

            for category, items in categories.items():
                f.write(f"\n{category.upper()}:\n")

                correct_in_category = 0
                for request, result in items:
                    status = "✓" if result['correct'] else "✗"
                    if result['correct']:
                        correct_in_category += 1

                    f.write(f"{status} {request}\n")
                    if not result['correct']:
                        f.write(f"   Ожидалось: {result['expected']}\n")
                        f.write(f"   Получено: {result['actual']}\n")

                f.write(
                    f"\nТочность в категории: {correct_in_category}/{len(items)} ({correct_in_category / len(items):.1%})\n")

        print("РЕЗУЛЬТАТЫ ПОИСКА ЛУЧШЕГО КОЭФФИЦИЕНТА:")
        print(f"Лучший коэффициент: {best_rapid:.3f}")
        print(f"Максимальная точность: {best_accuracy:.2%}")
        print(f"Правильных ответов: {int(best_accuracy * total)}/{total}")
        print(f"Файл с детальными результатами: best_rapid_results.txt")

        print("\nОШИБКИ (если есть):")

        errors_found = False
        for request, result in best_results.items():
            if not result['correct']:
                errors_found = True
                print(f"✗ {request}")
                print(f"  Ожидалось: {result['expected']}")
                print(f"  Получено: {result['actual']}")
                print()

        if not errors_found:
            print("Ошибок не обнаружено! Отличный результат!")


        # for request, expected in tests:
        #     assert query.get_intent(request, best_rapid) == expected