import threading, time
import requests

link = "https://Discord-Reminder-Bot.faiznc.repl.co"
link2 = "http://172.18.0.7:8080/"


def print_every_n_seconds(n=60):
    while True:
        print(time.ctime())
        time.sleep(n)
    
thread1 = threading.Thread(target=print_every_n_seconds, daemon=True)

def reopen_link(n=60):
    while True:
        print(time.ctime())
        r = requests.get(link)
        # print(r.content)
        time.sleep(n)

thread_web = threading.Thread(target=reopen_link, daemon=True)

def start_timer():
  thread1.start()
  thread_web.start()