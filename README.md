
 

1 -- скачиваете докер (лучше Docker-Desktop)

2 -- docker compose up -d

3 -- бд работает на 5432 порту - если у вас на этом же порту работет ваша бд то еужно либо оффеуть ее или в docker-compose указать 5433:5432

4 -- перезапустить контейнер migrations (он почему то отваливается при запуске)

5 -- весь бек доступен по префиксу api/v1 - за документацией по каждому из серисов обращаться по http://localhost:8000/{то что написанно для каждого сервиса в nginx_config}/docs