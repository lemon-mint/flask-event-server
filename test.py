import secrets
import requests
import time


chid = secrets.token_hex(16)
trycount = 1

while True:
    try:
        print("Try : {}".format(trycount))
        resp = requests.get('http://127.0.0.1:32729/calc/{}'.format(chid))
        if resp.status_code == 200:
            break
    except:
        trycount += 1
        time.sleep(1)

# /calc/<ch name> test
resp = requests.get('http://127.0.0.1:32729/calc/{}'.format(chid))
if resp.status_code == 200:
    chid_hash = resp.text
    resp = requests.get('http://127.0.0.1:32729/sse/deploy/{}'.format(chid))
    assert resp.status_code == 200
    exit(1)
else:
    exit(-1)
exit(-1)
