import torch
import os
import zipfile
import shutil


def download_silero_model():
    """Скачивает и сохраняет модель Silero локально"""
    model_dir = os.path.join(os.path.dirname(__file__), 'models', 'silero')
    os.makedirs(model_dir, exist_ok=True)

    print("Скачивание модели Silero...")

    # Загружаем модель через hub
    model, example_text = torch.hub.load(
        repo_or_dir='snakers4/silero-models',
        model='silero_tts',
        language='ru',
        speaker='v3_1_ru',
        force_reload=True  # Принудительная загрузка
    )

    # Сохраняем модель как полный пакет
    model_path = os.path.join(model_dir, 'silero_model.pth')

    # Сохраняем словарь с моделью и дополнительной информацией
    torch.save({
        'model_state_dict': model.state_dict(),
        'speaker': 'v3_1_ru',
        'language': 'ru',
        'sample_rate': 48000
    }, model_path)

    print(f"Модель сохранена в {model_path}")

    # Также сохраняем пример текста
    with open(os.path.join(model_dir, 'example_text.txt'), 'w', encoding='utf-8') as f:
        f.write(example_text)

    return model_path


def download_model_alternative():
    import urllib.request

    model_dir = os.path.join(os.path.dirname(__file__), 'models', 'silero')
    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, 'v3_1_ru.pt')

    if not os.path.exists(model_path):
        print("Скачивание модели напрямую...")
        url = "https://models.silero.ai/models/tts/ru/v3_1_ru.pt"
        try:
            urllib.request.urlretrieve(url, model_path)
            print(f"Модель скачана в {model_path}")
            return model_path
        except Exception as e:
            print(f"Ошибка при скачивании: {e}")
            return None
    else:
        print("Модель уже существует")
        return model_path


if __name__ == "__main__":
    try:
        download_silero_model()
    except Exception as e:
        print(f"Первый способ не сработал: {e}")
        print("Пробуем альтернативный способ...")
        download_model_alternative()