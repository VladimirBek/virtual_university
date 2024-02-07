### Запуск приложения в docker:
Для работы с переменными окружениями необходимо создать файл .env и заполнить его слеующими переменными


- POSTGRES_USER=
- POSTGRES_PASSWORD=
- POSTGRES_DB=
- STRIPE_API_KEY
- STRIPE_URL


_Для создания образа из Dockerfile и запуска контейнера запустить команду:_
```
docker-compose up --build
```
 или
 ```
docker-compose up -d --build
