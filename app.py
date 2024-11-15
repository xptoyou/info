from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, send
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Initialize Flask app and extensions
app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)
login_manager = LoginManager(app)

# Simulate a database of users
users = {'admin': {'password': 'adminpass', 'role': 'admin'},
         'guest': {'password': 'guestpass', 'role': 'guest'}}

class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role

# User loader for Flask-Login
@login_manager.user_loader
def load_user(username):
    user_info = users.get(username)
    if user_info:
        return User(username, user_info['role'])
    return None

@app.route('/')
def index():
    return render_template('login.html')  # Login page

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user_info = users.get(username)

    if user_info and user_info['password'] == password:
        user = User(username, user_info['role'])
        login_user(user)
        return redirect(url_for('chat'))
    return 'Invalid credentials!'

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@socketio.on('message')
def handle_message(msg):
    if current_user.role == 'admin':
        send(msg, broadcast=True)  # Admin can broadcast messages
    else:
        send('You are not allowed to send messages.', room=request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)

