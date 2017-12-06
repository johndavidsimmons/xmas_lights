from flask import Flask, render_template
from raspberry import RaspberryThread
from light_functions import blink_all, all_pins_off, lightshow, cycle_all
from xmas import russian_xmas
import os

# Load the env variables
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/blink", methods=['GET'])
def blink_view():
    # Pause any running threads
    any(thread.pause() for thread in threads)

    # Start the target thread if it is not running
    if not blink_thread.isAlive():
        blink_thread.start()
    # Unpause the thread and thus execute its function
    blink_thread.resume()
    return "blink started"


@app.route("/cycleall", methods=["GET"])
def cycleall_view():
    any(thread.pause() for thread in threads)
    if not cycle_all_thread.isAlive():
        cycle_all_thread.start()
    cycle_all_thread.resume()
    return "cycle all started"


@app.route("/lightshow", methods=["GET"])
def lightshow_view():
    any(thread.pause() for thread in threads)
    if not lightshow_thread.isAlive():
        lightshow_thread.start()
    lightshow_thread.resume()
    return "lightshow started"


@app.route("/russianxmas", methods=["GET"])
def russianxmas_view():
    any(thread.pause() for thread in threads)
    if not russian_xmas_thread.isAlive():
        russian_xmas_thread.start()
    russian_xmas_thread.resume()
    return "russian xmas started"


@app.route("/shutdown", methods=['GET'])
def shutdown():
    all_pins_off()
    any(thread.pause() for thread in threads)
    return "all threads paused"


if __name__ == '__main__':
    # Create threads
    blink_thread = RaspberryThread(function=blink_all)
    lightshow_thread = RaspberryThread(function=lightshow)
    russian_xmas_thread = RaspberryThread(function=russian_xmas)
    cycle_all_thread = RaspberryThread(function=cycle_all)

    # collect threads
    threads = [
        blink_thread,
        lightshow_thread,
        russian_xmas_thread,
        cycle_all_thread
    ]

    # Run server
    app.run(
        debug=True,
        host=os.environ.get("IP_ADDRESS"),
        port=int(os.environ.get("PORT")),
        threaded=True)
