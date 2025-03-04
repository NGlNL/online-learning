## Docker

### Шаги для запуска

1. Убедитесь, что у вас установлен Docker
2. Скопируйте файл `.env.example` в `.env` и заполните его вашими данными.
3. В корне проекта выполните команду:

   ```bash
   docker-compose up -d --build
   ```
4. После успешного запуска вы сможете проверить работоспособность сервисов:

Бэкенд: Перейдите по адресу http://localhost:8000
PostgreSQL: Подключитесь к базе данных на localhost:5432 с использованием указанных в .env данных.
Redis: Используйте redis-cli для подключения к localhost:6379.
Celery и Celery Beat: Логи можно просмотреть через docker-compose logs или подключившись к контейнерам.
### Остановка проекта
Чтобы остановить проект, выполните:
```bash
docker-compose down
````
# CI/CD для Django

Этот проект использует GitHub Actions для непрерывной интеграции и развертывания Django-приложения.

## Предисловие

1. **Репозиторий GitHub**: Создайте репозиторий на GitHub для своего Django-проекта.
2. **Учетная запись Docker Hub**: Создайте аккаунт на Docker Hub для pushes и pulls Docker-изображений.
3. **Удаленный сервер**: Настройте удаленный сервер с установленным Docker для развертывания приложения.
4. **Секреты**: Установите следующие секреты в настройках своего репозитория GitHub:
   - `SECRET_KEY`: Ключ секрета вашего Django-проекта.
   - `DOCKER_HUB_USERNAME`: Ваш логин на Docker Hub.
   - `DOCKER_HUB_ACCESS_TOKEN`: Личный токен доступа Docker Hub с правами чтения и записи.
   - `SSH_KEY`: Приватный ключ для доступа по SSH к вашему удаленному серверу.
   - `SSH_USER`: Логин для доступа по SSH к вашему удаленному серверу.
   - `SERVER_IP`: IP-адрес или hostname вашего удаленного сервера.
   - `DEPLOY_DIR`

## Настройка

1. **Создайте файл requirements.txt**: Перечислите все необходимые Python-пакеты для вашего Django-проекта в файле `requirements.txt`.
2. **Создайте Dockerfile**: В корневой директории проекта создайте файл `Dockerfile` со следующим содержанием:

```Dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update \
  && apt-get install -y gcc libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/\*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
```
Рабочий процесс GitHub Actions автоматически собирает, тестирует и развертывает ваше Django-приложение при push'е изменений в репозиторий или при создании pull request.

Рабочий процесс выполняет следующие задачи:

Лентинг (Linting): Запускает flake8 для проверки кода Python.
Тестирование: Настраивает окружение Python, устанавливает зависимости и запускает тесты с помощью python manage.py test.
Сборка: Собирает Docker-образ и отправляет его на Docker Hub.
Развертывание: Загружает Docker-образ с Docker Hub и запускает его на удаленном сервере.
