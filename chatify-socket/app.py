
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')
@socketio.on('connect')
def connect():
    print('Client %s connected' % request.sid)
@socketio.on('disconnect')
def disconnect(reason):
    print(f'Client {request.sid} disconnect with reason {reason}')
@socketio.on('newMessage')
def new_message(data):
    socketio.emit("newMessage", data)
@socketio.on('newConversation')
def new_conversation(data):
    socketio.emit("newConversation", data)
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)