from flask import Flask, render_template, jsonify, redirect, url_for, request, flash
from flask_socketio import SocketIO
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import abort
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key_123')
app.config['SESSION_PROTECTION'] = 'strong'  # Усиленная защита сессии

# Инициализация SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Настройка Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'

# Моковая база пользователей (в реальном проекте замените на БД)
users = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'role': 'admin'
    },
    'user': {
        'password': generate_password_hash('user123'),
        'role': 'user'
    }
}


class User(UserMixin):
    def __init__(self, id, role='user'):
        self.id = id
        self.role = role

    def is_admin(self):
        return self.role == 'admin'

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id, users[user_id]['role'])
    return None


# Маршруты аутентификации
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Если пользователь уже авторизован - перенаправляем на главную
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Проверяем существование пользователя
        if username not in users:
            flash('Неверное имя пользователя или пароль', 'danger')
            return redirect(url_for('login'))

        # Проверяем пароль
        user_data = users[username]
        if not check_password_hash(user_data['password'], password):
            flash('Неверное имя пользователя или пароль', 'danger')
            return redirect(url_for('login'))

        # Если все проверки пройдены - авторизуем пользователя
        user = User(username, user_data['role'])
        login_user(user)
        flash('Вы успешно вошли в систему', 'success')
        next_page = request.args.get('next')
        return redirect(next_page or url_for('home'))

    # GET-запрос - показываем форму входа
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))


# Моковые данные устройств
devices = [
    {"id": 1, "name": "Кухонный свет", "type": "light", "status": "on", "location": "kitchen"},
    {"id": 2, "name": "Термостат", "type": "thermostat", "status": "off", "location": "living_room"}
]


# Защищенные маршруты
@app.route('/')
@login_required
def home():
    return render_template('dashboard.html',
                           online_devices=len([d for d in devices if d['status'] == 'on']),
                           offline_devices=len([d for d in devices if d['status'] == 'off']),
                           username=current_user.id)


@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin():
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('home'))
    return render_template('admin.html', users=users)  # Добавили users в контекст

@app.route('/add-device')
@login_required
def add_device():
    return render_template('add_device.html')

@app.route('/dev_mode')
@app.route('/developer')  # Оба URL ведут на одну страницу
@login_required
def dev_mode():
    if not current_user.is_admin():
        flash('Доступ только для разработчиков', 'danger')
        return redirect(url_for('home'))
    return render_template('dev_mode.html')

@app.route('/automation')
@login_required
def automation():
    return render_template('automation.html')

@app.route('/devices')
@login_required
def devices_page():
    return render_template('devices.html', devices=devices)

@app.route('/api/devices/<int:device_id>/<action>')
@login_required
def device_action(device_id, action):
    device = next((d for d in devices if d['id'] == device_id), None)
    if device:
        device['status'] = 'on' if action == 'turn_on' else 'off'
        socketio.emit('device_update', device)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404


# Обработчики SocketIO
@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        print(f'Клиент подключен: {current_user.id}')
    else:
        return False  # Отклоняем неаутентифицированные подключения


@socketio.on('disconnect')
def handle_disconnect():
    print('Клиент отключен')


if __name__ == '__main__':
    socketio.run(app,
                 debug=True,
                 allow_unsafe_werkzeug=True,
                 host='localhost',
                 port=5000)