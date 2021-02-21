import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify
from video_feed import VideoCamera
import socketio

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
camera = VideoCamera()
sio = socketio.Client()
thread = None


@app.route('/connect', methods=["POST"])
def connect_with_server():
    try:
        sio.connect('http://localhost:5000/camera')
        print('Connected')
        return jsonify(success=True), 200
    except socketio.exceptions.ConnectionError as e:
        print('Connection failed')
        print(e)
        return jsonify(success=False), 500


@app.route('/start_feed', methods=["POST"])
def start_feed():
    if not camera.is_opened:
        camera.open()
        global thread
        thread = sio.start_background_task(emit_feed)
        print('Camera opened')
        return jsonify(success=True), 200
    return jsonify(success=False), 403


@app.route('/stop_feed', methods=["POST"])
def stop_feed():
    camera.close()
    print('Camera closed')
    return jsonify(success=True), 200


@app.route('/disconnect', methods=["POST"])
def disconnect():
    sio.disconnect()
    print('Camera disconnected')
    return jsonify(success=True), 200


def emit_feed():
    while camera.is_opened:
        frame = camera.get_frame()
        bytes_frame = frame.tobytes()
        sio.emit('byte_feed', {'bytes': bytes_frame})
        sio.sleep(0)
    global thread
    thread.join()
    print('Background task ended')


if __name__ == '__main__':
    Flask.run(app, host='0.0.0.0', port=5001)
