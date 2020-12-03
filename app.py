import hashlib
import json
import os
import secrets
import time
import base64

from flask import (Flask, Request, Response, flash, jsonify, redirect,
                   render_template)
from flask import request as f_req
from flask import request as fr
from flask import send_from_directory, session

import sse

app = Flask(__name__)

msgq = sse.MQSSE()


def make_event(data: dict, event=None) -> str:
    msg = 'data: {}\n\n'.format(json.dumps(data))
    if event:
        msg = 'event: {}\n{}'.format(event, msg)
    msg = 'id: {}\n{}'.format(data['eventid'], msg)
    return msg


@app.route('/sse/listen/<ch>')
def sse_abcd(ch):
    def stream(ch):
        messages = msgq.listen(ch)
        yield ":ok\n\n"
        while True:
            msg = messages.get()
            yield msg
    resp = Response(stream(ch), mimetype='text/event-stream')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/sse/deploy/<ch>')
def sse_deploy(ch):
    try:
        if fr.args.get('sub'):
            event_type = int(fr.args.get('sub'))
        else:
            event_type = 9999
        curtime = time.time()
        eventid = secrets.token_hex(10)
        if fr.args.get('type') and 0 < len(str(fr.args.get('type'))) and len(str(fr.args.get('type'))) < 16:
            eventname = str(fr.args.get('type'))
            msg = make_event(
                data={
                    'time': curtime,
                    'eventid': eventid,
                    'sub': event_type
                },
                event=eventname
            )
        else:
            msg = make_event(
                data={
                    'time': curtime,
                    'eventid': eventid,
                    'sub': event_type
                }
            )
        msgq.deploy(msg, hashlib.sha384(str(ch).encode('ascii')).hexdigest())
        return jsonify(
            {
                'success': True,
                'time': curtime,
                'eventid': eventid,
                'sub': event_type
            }
        ), 200
    except:
        pass
    return jsonify(
        {
            'success': False
        }
    ), 500


@app.route('/sse/redirect/<ch>/<url>')
def deploy_and_redirect(ch, url):
    msg = make_event(
        data={
            'time': time.time(),
            'eventid': secrets.token_hex(10),
            'sub': 9999
        }
    )
    msgq.deploy(msg, hashlib.sha384(str(ch).encode('ascii')).hexdigest())
    print(url)
    return redirect(base64.urlsafe_b64decode(url).decode('utf-8'))

@app.route('/calc/<ch>')
def calc(ch):
    return hashlib.sha384(str(ch).encode('ascii')).hexdigest()


@app.route('/sse/test')
def testpage():
    return render_template('sse.html')


@app.route('/favicon.ico')
def __favicon__():
    return send_from_directory('.', 'favicon.ico')


@app.route('/')
def __index_html__():
    return send_from_directory('.', 'index.html')


@app.route('/robots.txt')
def __robots_txt__():
    return send_from_directory('.', 'robots.txt')


if __name__ == "__main__":
    from cheroot.wsgi import PathInfoDispatcher as WSGIPathInfoDispatcher
    from cheroot.wsgi import Server as WSGIServer
    my_app = WSGIPathInfoDispatcher({'/': app})
    server = WSGIServer(
        ('0.0.0.0', int(os.environ.get('PORT', 32729))), my_app)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
