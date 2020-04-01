# smtp2pushover
Receives any SMTP mail on port 10025 and redirect it to a pushover device.

## To use:
Create pushover_credentials.py with content:
```
TOKEN='yourpushovertoken'
USER='yourpushoveruser'
```
Install necessary modules
```
pip install -r requirements.txt
```
Run it 
```
python smtpsink.py
```
or run it with Docker
```
docker run -it --rm --name smtp2pushover -v "$PWD":/root -w /root python:3-alpine pip3 install --user -r requirements.txt
docker run -it -d --rm --name smtp2pushover -p 25:10025 -v "$PWD":/root -w /root python:3-alpine python smtpsink.py
```
