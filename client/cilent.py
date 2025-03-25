import uuid
import socketio

if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect('http://192.168.2.14:5002')
    sio.emit('check-in', {'user_id': str(uuid.uuid1())})
    sio.wait()