import os
import urllib.request
import zipfile
import shutil


def download_large_vosk_model(language="ru"):
    """
    Скачивание большой модели Vosk для указанного языка

    :param language: язык модели ("ru" или "en")
    """

    # URL-ы для больших моделей Vosk
    MODEL_URLS = {
        "ru": "https://alphacephei.com/vosk/models/vosk-model-ru-0.10.zip",
        "en": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
    }

    # Названия папок после распаковки
    MODEL_DIRS = {
        "ru": "vosk-model-ru-0.10",
        "en": "vosk-model-en-us-0.22"
    }

    if language not in MODEL_URLS:
        print(f"Язык {language} не поддерживается. Доступны: ru, en")
        return False

    # Создание папки для моделей
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)

    model_url = MODEL_URLS[language]
    model_dir_name = MODEL_DIRS[language]
    model_path = os.path.join(models_dir, model_dir_name)

    # Проверка, не скачана ли уже модель
    if os.path.exists(model_path):
        print(f"Модель для языка {language.upper()} уже существует в {model_path}")
        choice = input("Хотите скачать заново? (y/n): ").lower()
        if choice != 'y':
            print("Скачивание отменено")
            return True

    zip_path = os.path.join(models_dir, f"vosk-model-{language}-large.zip")

    print(f"=" * 60)
    print(f"СКАЧИВАНИЕ БОЛЬШОЙ МОДЕЛИ VOSK ДЛЯ ЯЗЫКА: {language.upper()}")
    print(f"=" * 60)
    print(f"URL: {model_url}")
    print(f"Размер: ~2 GB")
    print(f"Место назначения: {model_path}")
    print(f"Это может занять много времени...")
    print(f"=" * 60)

    try:
        # Функция для отображения прогресса
        def progress_callback(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = downloaded * 100 / total_size
                downloaded_mb = downloaded / (1024 * 1024)
                total_mb = total_size / (1024 * 1024)

                # Создание прогресс-бара
                bar_length = 40
                filled_length = int(bar_length * downloaded // total_size)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)

                print(f'\rПрогресс: |{bar}| {percent:.1f}% ({downloaded_mb:.1f} MB / {total_mb:.1f} MB)', end='')

        # Скачивание файла
        print("Начинаю скачивание...")
        urllib.request.urlretrieve(model_url, zip_path, progress_callback)
        print("\n✅ Скачивание завершено!")

        # Проверка размера скачанного файла
        file_size = os.path.getsize(zip_path) / (1024 * 1024)
        print(f"Размер скачанного файла: {file_size:.1f} MB")

        # Распаковка
        print("\n📦 Распаковка модели...")

        # Создание временной папки для распаковки
        extract_temp = os.path.join(models_dir, "temp_extract")
        os.makedirs(extract_temp, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Получение списка файлов для отображения прогресса
            file_list = zip_ref.namelist()
            total_files = len(file_list)

            for i, file in enumerate(file_list, 1):
                zip_ref.extract(file, extract_temp)
                if i % 10 == 0:  # Обновление каждые 10 файлов
                    print(f"\rРаспаковано: {i}/{total_files} файлов", end='')

        print(f"\r✅ Распаковано: {total_files}/{total_files} файлов")

        # Перемещение распакованной модели
        extracted_path = os.path.join(extract_temp, model_dir_name)
        if os.path.exists(model_path):
            shutil.rmtree(model_path)
        shutil.move(extracted_path, model_path)

        # Удаление временных файлов
        shutil.rmtree(extract_temp)
        os.remove(zip_path)

        print(f"✅ Модель успешно установлена в: {model_path}")

        # Проверка структуры модели
        required_files = ["am", "conf", "ivector", "graph", "README.md", "spk_vector"]
        missing_files = []

        for req_file in required_files:
            if not os.path.exists(os.path.join(model_path, req_file)) and \
                    not os.path.exists(os.path.join(model_path, req_file + ".conf")):
                missing_files.append(req_file)

        if missing_files:
            print(f"⚠️  Внимание: отсутствуют некоторые компоненты: {missing_files}")
        else:
            print("✅ Структура модели корректна")

        # Показ содержимого модели
        print(f"\n📁 Содержимое модели:")
        for item in os.listdir(model_path):
            item_path = os.path.join(model_path, item)
            if os.path.isdir(item_path):
                size = sum(os.path.getsize(os.path.join(item_path, f)) for f in os.listdir(item_path)
                           if os.path.isfile(os.path.join(item_path, f))) / (1024 * 1024)
                print(f"  📁 {item}/ ({size:.1f} MB)")
            else:
                size = os.path.getsize(item_path) / 1024
                print(f"  📄 {item} ({size:.1f} KB)")

        return True

    except urllib.error.URLError as e:
        print(f"\n❌ Ошибка сети: {e}")
        print("Проверьте подключение к интернету")
        return False
    except zipfile.BadZipFile as e:
        print(f"\n❌ Ошибка распаковки: {e}")
        print("Возможно, файл был скачан повреждённым")
        return False
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        return False
    finally:
        # Очистка временных файлов в случае ошибки
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except:
                pass
        if os.path.exists(os.path.join(models_dir, "temp_extract")):
            try:
                shutil.rmtree(os.path.join(models_dir, "temp_extract"))
            except:
                pass


def check_disk_space(required_mb=2500):
    """
    Проверка свободного места на диске

    :param required_mb: требуемое место в MB
    :return: достаточно ли места
    """
    import shutil

    total, used, free = shutil.disk_usage(".")
    free_mb = free / (1024 * 1024)

    print(f"Свободное место на диске: {free_mb:.1f} MB")

    if free_mb < required_mb:
        print(f"⚠️  Недостаточно места! Требуется минимум {required_mb} MB")
        return False
    return True


def main():
    """
    Главная функция для скачивания большой модели
    """
    print("=" * 60)
    print("СКАЧИВАНИЕ БОЛЬШОЙ МОДЕЛИ VOSK")
    print("=" * 60)

    # Проверка свободного места
    if not check_disk_space():
        choice = input("Продолжить всё равно? (y/n): ").lower()
        if choice != 'y':
            return

    # Выбор языка
    print("\nДоступные языки:")
    print("1. Русский (ru) - ~2 GB")
    print("2. Английский (en) - ~2 GB")

    choice = input("\nВыберите язык (1/2) [1]: ").strip() or "1"

    if choice == "1":
        language = "ru"
    elif choice == "2":
        language = "en"
    else:
        print("Неверный выбор")
        return

    # Скачивание модели
    success = download_large_vosk_model(language)

    if success:
        print("\n" + "=" * 60)
        print("✅ МОДЕЛЬ УСПЕШНО УСТАНОВЛЕНА!")
        print("=" * 60)
        print(f"\nПуть к модели: models/vosk-model-{language}-0.10")
        print("\nТеперь вы можете использовать её для распознавания речи:")
        print("""
from vosk import Model, KaldiRecognizer
import wave
import json

# Загрузка модели
model = Model("models/vosk-model-{}-0.10")
rec = KaldiRecognizer(model, 16000)

# Распознавание из файла
with wave.open("audio.wav", "rb") as wf:
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print(result["text"])
""".format(language))
    else:
        print("\n❌ Не удалось установить модель")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Скачивание прервано пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")