import asyncio
import os
import re

import ebooklib
import edge_tts
from bs4 import BeautifulSoup
from ebooklib import epub

# --- НАСТРОЙКИ ---
EPUB_FILE = "book.epub"  # Имя вашего файла (измените при необходимости)
OUTPUT_DIR = "audio_chapters"  # Папка, куда сохранятся MP3
VOICE = (
    "ru-RU-DmitryNeural"  # Голос: Dmitry (мужской) или ru-RU-SvetlanaNeural (женский)
)
# -----------------

# Создаем папку для вывода, если её нет
os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_html(html_content):
    """Удаляет HTML-теги и лишние пробелы, оставляя чистый текст"""
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    # Убираем множественные пробелы и странные символы
    text = re.sub(r"\s+", " ", text)
    return text


async def generate_audio(text, filename):
    """Генерирует MP3 из текста с помощью edge-tts"""
    if (
        not text or len(text) < 50
    ):  # Пропускаем слишком короткие фрагменты (пустые главы)
        print(f"Пропуск: {filename} (слишком мало текста)")
        return

    print(f"Озвучиваю: {filename}... (длина текста: {len(text)} симв.)")
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(os.path.join(OUTPUT_DIR, filename))
        print(f"✓ Готово: {filename}")
    except Exception as e:
        print(f"✗ Ошибка при озвучке {filename}: {e}")


async def main():
    print(f"Читаем файл: {EPUB_FILE}")
    try:
        book = epub.read_epub(EPUB_FILE)
        # Сразу узнаем количество
        docs = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        total = len(docs)
        print(f"Всего нужно обработать: {total} файлов\n")
    except FileNotFoundError:
        print(f"Ошибка: Файл '{EPUB_FILE}' не найден. Проверьте имя файла.")
        return

    chapter_counter = 1
    # Перебираем все элементы книги
    for item in book.get_items():
        # Нас интересуют только элементы с текстом (DOCUMENT)
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Получаем HTML-содержимое главы
            html_content = item.get_content().decode("utf-8")
            clean_text = clean_html(html_content)

            # Формируем имя файла. Используем заголовок из EPUB, если он есть, иначе просто номер
            title = item.get_name().replace(".xhtml", "").replace(".html", "")
            # Очищаем имя файла от недопустимых в Linux/Windows символов
            safe_title = re.sub(r'[\\/*?:"<>|]', "", title).strip()
            if not safe_title:
                safe_title = f"chapter_{chapter_counter}"

            filename = f"{chapter_counter:02d}_{safe_title}.mp3"

            await generate_audio(clean_text, filename)
            chapter_counter += 1

    print("\n🎉 Все готово! Аудиофайлы сохранены в папке:", os.path.abspath(OUTPUT_DIR))


if __name__ == "__main__":
    # Сразу узнаем количество
    asyncio.run(main())
