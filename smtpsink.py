from datetime import datetime
import pytz
from time import sleep
import asyncore
from smtpd import SMTPServer
import socket
import requests
from pushover_credentials import TOKEN, USER
import threading

wtapi = requests.get("http://worldtimeapi.org/api/ip")
tz = pytz.timezone(wtapi.json()["timezone"])
#tz = pytz.timezone('Europe/Stockholm')

class EmlServer(SMTPServer):
    print('Ready!')
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        datevar = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        print('Message was recived ' + datevar)
        self.data = str(data)
        thread = threading.Thread(target=self.pushover, args=())
        thread.daemon = True
        thread.start()
        print('Handling Done! Replying 250 to client')

    def pushover(self):
        pushover_data = {
            'token': (None, TOKEN),
            'user': (None, USER),
            'message': (None, self.data),
        }
        h = datetime.now(tz).strftime('%H')
        if int(h) < 7:
            print('delaying...')
            sleephour = 7-int(h)
            sleep(sleephour*60*60)
        elif int(h) > 22:
            print('delaying...')
            sleep(8*60*60)
        print('Sending message!')
        requests.post('https://api.pushover.net/1/messages.json', files=pushover_data)

def run():
    EmlServer((socket.gethostbyname(socket.gethostname()), 10025) , None, decode_data=True)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    run()
