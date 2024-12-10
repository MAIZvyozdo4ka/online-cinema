
 

- скачиваете докер (лучше Docker-Desktop)

- Разархивируем ```.csv``` данные из архива
```bash 
./install.sh
```

- Поднимаем контейнер
```bash 
docker compose up -d
```

- бд работает на 5432 порту - если у вас на этом же порту работет ваша бд то еужно либо оффеуть ее или в docker-compose указать 5432:5432

5 -- весь бек доступен по префиксу api/v1 - за документацией по каждому из серисов обращаться по http://localhost:8000/{то что написанно для каждого сервиса в nginx_config}/docs

6 -- admin password - qKXxzXwQ , login - main_admin

7 -- в s3-init создать папку movie_mp4 d нее файлы с фильмами и файл movie.csv с movie_id,"file_path"