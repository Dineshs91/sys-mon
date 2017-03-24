import psutil
from flask import Flask
from flask import jsonify

app = Flask(__name__)


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
    return "Hello world"


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
    cpu_dict = {
        'times': psutil.cpu_times(),
        'percent': psutil.cpu_percent(),
        'count': psutil.cpu_count()
    }

    return jsonify(cpu_dict)


if __name__ == "__main__":
    app.run()

