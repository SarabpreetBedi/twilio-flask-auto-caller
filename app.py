from flask import Flask, request, render_template
from call_manager import make_call
from call_status_db import update_status, get_all_calls, init_db
import csv
import os
import threading
from datetime import datetime

app = Flask(__name__)

init_db()

@app.context_processor
def inject_now():
    return {'now': datetime.now}

@app.route('/')
def dashboard():
    calls = get_all_calls()
    return render_template("dashboard.html", calls=calls)

@app.route('/start')
def start_calls():
    with open("numbers.csv") as f:
        numbers = [line.strip() for line in f.readlines()]

    for i, num in enumerate(numbers):
        threading.Thread(target=make_call, args=(num, f"Call-{i+1}")).start()

    return "Calls are being made!"

@app.route("/status", methods=["POST"])
def status():
    sid = request.form.get("CallSid")
    status = request.form.get("CallStatus")
    update_status(sid, status)
    return '', 204

@app.route("/voice", methods=["POST"])
def voice():
    return '''
    <Response>
        <Gather action="/handle_key" method="POST" numDigits="1">
            <Say>Press 1 to talk to an agent</Say>
        </Gather>
    </Response>
    '''

@app.route("/handle_key", methods=["POST"])
def handle_key():
    digit = request.form.get("Digits")
    if digit == "1":
        return f'''
        <Response>
            <Dial>{os.getenv("AGENT_NUMBER")}</Dial>
        </Response>
        '''
    else:
        return '''
        <Response>
            <Say>Invalid input</Say>
        </Response>
        '''

if __name__ == "__main__":
    app.run(debug=True)
