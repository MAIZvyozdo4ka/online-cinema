## Новая работа с .csv (и другими большими файлами, если будут).

### Установка `Git-lfs`

```bash
sudo apt-get install git-lfs
```

### Клонирование репозитория с `Git-LFS`

```bash
git lfs clone https://example.com/user/repo.git
```

### Локальная инициализация `Git-LFS`

```bash
git lfs install
```

### Файлы можно подтянуть принудительно из текущей ветки.

```bash
git lfs pull
```