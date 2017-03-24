import eventlet
import psutil
from flask import Flask, render_template
from flask import jsonify
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET!!!'
socketio = SocketIO(app)


@app.route("/")
def home():
    """
    Categories:
    1. Process
    2. Memory
    3. Disk
    4. Users
    5. cpu
    """
    return render_template("index.html")


@app.route("/proc")
def process():
    proc_dict = {
        "pids": psutil.pids(),
    }

    return jsonify(proc_dict)


@app.route("/mem")
def memory():
    memory_dict = {
        'virtual': psutil.virtual_memory(),
        'swap': psutil.swap_memory()
    }

    return jsonify(memory_dict)


@app.route("/disk")
def disk():
    disk_dict = {
        'partitions': psutil.disk_partitions(),
        'disk_usage': psutil.disk_usage('/')
    }

    return jsonify(disk_dict)


@app.route("/users")
def users():
    return jsonify(psutil.users())


@app.route("/cpu")
def cpu():
    cpu_dict = get_cpu_stats()

    return jsonify(cpu_dict)


def get_cpu_stats():
    cpu_dict = {
        'times': psutil.cpu_times(),
        'percent': psutil.cpu_percent(),
        'count': psutil.cpu_count()
    }

    return cpu_dict


@socketio.on('start')
def start():
    eventlet.spawn(start_loop)


def start_loop():
    while True:
        socketio.emit('cpu_update', get_cpu_stats())
        eventlet.sleep(3)


if __name__ == "__main__":
    socketio.run(app)
