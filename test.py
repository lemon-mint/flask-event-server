import secrets
import requests

chid = secrets.token_hex(16)

# /calc/<ch name> test
resp = requests.get('127.0.0.1:32729/calc/{}'.format(chid))
print(resp.text)

exit(0)
