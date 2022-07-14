#!/usr/bin/python3
""" Prometheus Alert Telegram Bot  """

from os import environ as env
import telebot
import json_log_formatter  # Used in gunicorn_logging.conf
from flask import (
    Flask,
    request,
    make_response,
    abort
)
from flask_wtf.csrf import CSRFProtect
from prometheus_client import multiprocess, generate_latest, Summary, CollectorRegistry

app = Flask(__name__, template_folder="templates")
csrf = CSRFProtect()

app.config["TEABOT_DEFAULT_CHATID"] = str(env.get("TEABOT_DEFAULT_CHATID", ''))
app.config["TEABOT_TELEGRAM_TOKEN"] = str(env.get("TEABOT_TELEGRAM_TOKEN", ''))

REQUEST_TIME = Summary("svc_request_processing_time", "Time spent processing request")

bot = telebot.TeleBot(app.config["TEABOT_TELEGRAM_TOKEN"])

def telegram_send_message(chat_id,message):
    """ send message to telegram  """
    bot.send_message(chat_id, message)

def child_exit(server, worker):
    """ multiprocess function for prometheus to track gunicorn """
    multiprocess.mark_process_dead(worker.pid)

@app.route("/healthz", methods=["GET"])
def default_healthz():
    """ healthcheck route """
    return make_response('', 200)

@app.route("/metrics", methods=["GET"])
def metrics():
    """  metrics route """
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return generate_latest(registry)

@app.route("/", methods=["POST"])
@REQUEST_TIME.time()
def req_handler():
    """GET/PUT requests handler"""
    try:
        if request.method == "POST":
            content = request.get_json(silent=True)
            print (content)
            telegram_send_message(app.config["TEABOT_DEFAULT_CHATID"], content)
            return make_response('', 200)
        return make_response('', 405)
    except Exception as exp:
        print("Error in req_handler():"+ str(exp))
        return abort(500)

if __name__ == "__main__":
    app.run(threaded=True)
    csrf.init_app(app)
