from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ecret!'
socketio = SocketIO(app)

users = []

html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Real-time Chat App</title>
  <script src="https://cdn.jsdelivr.net/npm/socket.io@2.3.0/dist/socket.io.js"></script>
  <script>
    const socket = io();
    let username;

    document.addEventListener('DOMContentLoaded', () => {
      const usernameInput = document.getElementById('username');
      const joinBtn = document.getElementById('join-btn');
      const chatLog = document.getElementById('chat-log');
      const messageInput = document.getElementById('message');
      const sendBtn = document.getElementById('send-btn');

      joinBtn.addEventListener('click', () => {
        username = usernameInput.value;
        socket.emit('new-user', username);
        usernameInput.disabled = true;
        joinBtn.disabled = true;
      });

      sendBtn.addEventListener('click', () => {
        const message = messageInput.value;
        socket.emit('send-message', message);
        messageInput.value = '';
      });

      socket.on('new-user', (username) => {
        const message = `${username} has joined the chat`;
        chatLog.innerHTML += `<p>${message}</p>`;
      });

      socket.on('receive-message', (message) => {
        chatLog.innerHTML += `<p>${message}</p>`;
      });
    });
  </script>
</head>
<body>
  <h1>Real-time Chat App</h1>
  <input type="text" id="username" placeholder="Enter your username">
  <button id="join-btn">Join</button>
  <div id="chat-log"></div>
  <input type="text" id="message" placeholder="Enter your message">
  <button id="send-btn">Send</button>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html)

@socketio.on('connect')
def connect():
    print('New user connected')

@socketio.on('new-user')
def new_user(username):
    users.append(username)
    emit('new-user', username, broadcast=True)

@socketio.on('send-message')
def send_message(message):
    emit('receive-message', message, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    print('User disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)