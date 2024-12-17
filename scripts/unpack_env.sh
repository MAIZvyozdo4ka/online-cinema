#!/bin/bash

ZIP_FILES=(
    "data/s3_env.zip"
)

DEST_DIRS=(
    "core/env"
)

# Перебор архивов и директорий
for i in "${!ZIP_FILES[@]}"; do
    ZIP_FILE="${ZIP_FILES[i]}"
    DEST_DIR="${DEST_DIRS[i]}"

    # Проверка существования архива
    if [ ! -f "$ZIP_FILE" ]; then
        echo "Ошибка: Архив '$ZIP_FILE' не найден."
        continue
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
        echo "Архив '$ZIP_FILE' успешно распакован в '$DEST_DIR'."
    else
        echo "Ошибка при распаковке архива '$ZIP_FILE'."
    fi
done