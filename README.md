# IoT Control System Система управления IoT устройствами для локальных сетей
## Структура проекта
iot_system_kursovaya/
- │ .gitignore
- │ README.md
- │
- └───src
- │ .env - файл конфигурации
  - │ app.py - основной файл приложения
- │
- ├───static
- │ └───css
  - │ custom.css - кастомные стили
- └─── templates
  - │ add_device.html - добавление устройства
  - │ admin.html - админ-панель
  - │ automation.html - управление автоматизацией
  - │  base.html - базовый шаблон
  - │ dashboard.html - главная панель
  - │ devices.html - управление устройствами
  - │ dev_mode.html - режим разработчика
  - │ login.html - страница входа
  - │ voice.html - голосовое управление
  - └───js 
    - main.js - основные скрипты
## Установка и настройка
1. **Создание виртуального окружения**  
Выполните в командной строке:  
`python -m venv .venv`

2. **Активация окружения**  
Для Windows:  
`.venv\Scripts\activate`  
Для Linux/MacOS:  
`source .venv/bin/activate`

3. **Установка зависимостей**  
`pip install flask flask-login flask-socketio python-dotenv werkzeug`

4. **Генерация SECRET_KEY**  
Создайте ключ одним из способов:

   - Через Python-консоль (введите команды последовательно):
     ```python
     import secrets
     print(secrets.token_hex(24))
     ```

   - Или через командную строку:
     ```bash
     python -c "import secrets; print(secrets.token_hex(24))"
     ```

5. **Настройка окружения**  
Создайте файл `.env` в папке `src/` со следующим содержанием:
```
SECRET_KEY=сгенерированный_ключ_из_пункта_4
SESSION_PROTECTION=strong
```
6. **Запуск системы**  
Выполните:  
`python src/app.py`
7. **Доступ к системе**  
Откройте в браузере:  
`http://localhost:5000`
## Тестовые учетные данные
Для входа используйте:  
🔑 Администратор: `admin` / `admin123`  
👤 Обычный пользователь: `user` / `user123`