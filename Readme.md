API для сбора/показа/удаления статистики на FastAPI
===
Развернуть приложение:
----
1. Для запуска проекта с тестами через docker-compose в корне репозитория ввести команду: 

* docker-compose -f docker-compose.dev.yml up --build

2. Для запуска проекта без тестов через docker-compose:
* Поместить .fastapi.env и .postgres.env с вашими переменными в корень репозитория. 
  Список и пример переменных находится в файлах fastapi.sample.env и postgres.sample.env
  
* в корне репозитория ввести команду: docker-compose up --build

stats.DDL - файл для мануального создания таблицы в postgres
openapi.yaml - документация в формате openapi

Эндпоинты сервиса:
---
* /api/openapi - url документации сервиса вида openapi
* /api/vi/stats - url, который принимает запросы для сервиса.
Разрешенные методы: GET, POST, DELETE
  * Обязательные параметры GET запроса - start,end - дата в формате YYYY-MM-DD. Пример GET запроса: 
    
    * curl -X 'GET' \
  'http://{fastapi_host}:8010/api/v1/stats/?page=1&size=50&sort=date&start=2022-11-30&end=2022-11-30' \
  -H 'accept: application/json
  * Обязательное поле в теле запроса POST - date - дата в формате YYYY-MM-DD. Пример POST запроса:
    * curl -X 'POST' \
  'http://{fastapi_host}:8010/api/v1/stats/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "date": "2022-11-30",
  "views": 0,
  "clicks": 0,
  "cost": 0
}'
  * Пример DELETE запроса:
    * curl -X 'DELETE' \
  'http://{fastapi_host}:8010/api/v1/stats/' \
  -H 'accept: application/json'

