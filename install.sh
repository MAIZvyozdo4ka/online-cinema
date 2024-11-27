#!/bin/bash

# Указываем пути к архиву и директории внутри скрипта
ZIP_FILE="data/csv_data.zip"    # Путь к ZIP-архиву
DEST_DIR="migration/csv_data/"   # Путь к директории для распаковки

# Проверка существования архива
if [ ! -f "$ZIP_FILE" ]; then
    echo "Ошибка: Архив '$ZIP_FILE' не найден."
    exit 1
fi

# Проверка существования директории для распаковки
if [ ! -d "$DEST_DIR" ]; then
    echo "Директория '$DEST_DIR' не существует. Создаю её."
    mkdir -p "$DEST_DIR"
fi

# Распаковка архива
unzip "$ZIP_FILE" -d "$DEST_DIR"

# Проверка на успешность распаковки
if [ $? -eq 0 ]; then
    echo "Архив успешно распакован в '$DEST_DIR'."
else
    echo "Ошибка при распаковке архива."
    exit 1
fi
