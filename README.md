## BrainSystem

#### BrainSystem - сайт, посвященный изготовлению DIY брейн-системы для интеллектуальных игр.

##### Ресурсы сайта:

- Документация по сборке брейн-системы
- База данных вопросов
- API базы данных вопросов
- Telegram бот, подключенный к Базе

#### При разработке сайта применены следующие технологии:
- Python
- Django
- Django REST framework
- Redis
- Docker Compose
- PostgreSQL
- Nginx
- Gunicorn

#### Реализована контейнеризация отдельных компонентов проекта:
- Бэкенд
- Redis-сервер для кэширования
- База данных
- Веб-сервер
- Телеграм-бот

#### Комментарии к развертыванию проекта
- Переменнная DEVELOPMENT_SERVER файле .env отвечает за параметры запуска проекта:
    - DEVELOPMENT_SERVER=True - запуск проекта посредством docker compose; БД - PostgreSQL, кэширование - Redis;
    - DEVELOPMENT_SERVER=False - запуск сервера разработки; БД - SQLite, кэширование - File Based, email smtp-бэкенд отключен, captcha деактивирована для проведения автоматических тестов.
- Содержимое базы данных сохраняется в Docker Volumes.
- Оркестрация контейнеров реализована на базе Docker Compose.
- На сервере в домашней директории пользователя должна быть подготовлена директория "brain_system_django_docker".
- В эту директорию должен быть предварительно загружен файл .env с параметрами, не предполагающими общий доступ из репозитория.
- Необходимые переменные среды для файла .env указаны в файле .env.example.
- В директории `/infra` размещены инструкции docker compose:
    - `docker-compose_x86_64.yml` - для запуска на машине с архитектурой x86_64
    - `docker-compose_ARM64v8.yml` - для запуска на машине с архитектурой ARM64v8
    - развертывание проекта на production-сервере осуществляется согласно инструкции `docker-compose_ARM64v8.production.yml`. Инструкция предназначена для сервера с архитектурой ARM64v8.
- Перед развертыванием `docker-compose_ARM64v8.production.yml` необходимо:
    - собрать образы backend, tg_bot, nginx с учетом архитектуры сервера (выбрать соответствующий Dockerfile)
    - загрузить образы на Docker Hub
- После развертывания docker compose необходимо:
    - Запустить командную оболочку контейнера бэкенда: `sudo docker compose exec -it backend bash`
    - Выполнить миграции: `python3 manage.py migrate`
    - Собрать статику: `python3 manage.py collectstatic`
    - Перенести собранную статику в директорию, к которой подключен том docker volume: `cp -r collected_static/. production_static/`
