# Развертывание Telegram бота на Railway

## Подготовка к развертыванию

### 1. Создайте аккаунт на Railway
- Перейдите на [railway.app](https://railway.app)
- Войдите через GitHub
- Создайте новый проект

### 2. Подготовьте репозиторий
```bash
# Инициализируйте git если еще не сделали
git init
git add .
git commit -m "Initial commit for Railway deployment"

# Создайте репозиторий на GitHub и добавьте remote
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### 3. Настройте переменные окружения на Railway
В настройках проекта Railway добавьте следующие переменные:

- `BOT_TOKEN` - токен вашего Telegram бота
- `ADMIN_ID` - ваш Telegram ID
- `CHANNEL_1_ID` - ID первого канала
- `CHANNEL_2_ID` - ID второго канала  
- `CHANNEL_3_ID` - ID третьего канала
- `DATABASE_PATH` - путь к базе данных (оставьте bot_database.db)

### 4. Развертывание
1. Подключите ваш GitHub репозиторий к Railway
2. Railway автоматически определит Python проект
3. Дождитесь завершения сборки и развертывания

## Структура файлов для Railway

- `railway.json` - конфигурация Railway
- `Procfile` - команда запуска
- `runtime.txt` - версия Python
- `railway_start.py` - специальная версия main.py для Railway
- `requirements.txt` - зависимости Python

## Локальное тестирование

Для локального тестирования используйте:
```bash
python main.py
```

Для тестирования Railway версии:
```bash
python railway_start.py
```

## Мониторинг

После развертывания:
1. Проверьте логи в Railway Dashboard
2. Убедитесь, что бот отвечает в Telegram
3. Проверьте статус webhook

## Решение проблем

### Бот не отвечает
- Проверьте логи в Railway
- Убедитесь, что переменные окружения настроены правильно
- Проверьте, что бот добавлен как администратор в каналы

### Ошибки сборки
- Убедитесь, что все зависимости указаны в requirements.txt
- Проверьте версию Python в runtime.txt

### Проблемы с базой данных
- SQLite файл будет создан автоматически
- Для продакшена рекомендуется использовать PostgreSQL
