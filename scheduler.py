import schedule
import time
import requests

def job():
    print("Triggering auto-call job...")
    requests.get("http://localhost:5000/start")

schedule.every().day.at("14:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
