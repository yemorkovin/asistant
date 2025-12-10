from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib


class QuestionAnswerAssistant:
    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english', max_features=1000)),
            ('classifier', MultinomialNB())
        ])
        self.is_trained = False

    def train(self, questions, answers):
        """
        questions: список вопросов
        answers: список соответствующих ответов
        """
        X_train, X_test, y_train, y_test = train_test_split(
            questions, answers, test_size=0.2, random_state=42
        )

        self.pipeline.fit(X_train, y_train)
        self.is_trained = True

        # Оценка точности
        accuracy = self.pipeline.score(X_test, y_test)
        print(f"Точность модели: {accuracy:.2f}")

    def predict(self, question):
        if not self.is_trained:
            return "Модель не обучена. Сначала обучите модель."
        return self.pipeline.predict([question])[0]

    def save_model(self, filename):
        joblib.dump(self.pipeline, filename)
        print(f"Модель сохранена как {filename}")

    def load_model(self, filename):
        self.pipeline = joblib.load(filename)
        self.is_trained = True
        print(f"Модель загружена из {filename}")


# Пример использования
if __name__ == "__main__":
    # Пример данных для обучения
    questions = [
        "как тебя зовут",
        "сколько времени",
        "какая погода",
        "что ты умеешь",
        "помоги мне",
        "как дела",
        "расскажи шутку",
        "сколько будет 2+2",
        "кто твой создатель",
        "где ты находишься"
    ]

    answers = [
        "Я - ваш помощник, созданный с помощью sklearn",
        "Извините, у меня нет доступа к текущему времени",
        "Я не могу проверить погоду в реальном времени",
        "Я могу отвечать на вопросы и помогать с информацией",
        "Конечно, чем могу помочь?",
        "У меня всё отлично, спасибо! А у вас?",
        "Почему программист не носит очки? Потому что он C#!",
        "2+2=4",
        "Я создан с помощью библиотеки sklearn",
        "Я существую в цифровом пространстве"
    ]

    # Создание и обучение помощника
    assistant = QuestionAnswerAssistant()
    assistant.train(questions, answers)

    # Тестирование
    test_questions = [
        "привет",
        "здравствуй",
        "добрый день",

    ]

    for question in test_questions:
        answer = assistant.predict(question)
        print(f"Вопрос: {question}")
        print(f"Ответ: {answer}\n")