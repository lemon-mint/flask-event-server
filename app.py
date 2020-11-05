import json
import secrets
import time
import os
import hashlib

from flask import (Flask, Request, Response, flash, jsonify, redirect,
                   render_template)
from flask import request as f_req
from flask import request as fr
from flask import send_from_directory, session

import sse

app = Flask(__name__)

msgq = sse.MQSSE()


def make_event(data: dict, event="default") -> str:
    msg = f'data: {json.dumps(data)}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
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
        eventname = 'default'
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

@app.route('/calc/<ch>')
def calc(ch):
    return hashlib.sha384(str(ch).encode('ascii')).hexdigest()


@app.route('/sse/test')
def testpage():
    return render_template('sse.html')


@app.route('/favicon.ico')
def __favicon__():
    return send_from_directory('.','favicon.ico')


if __name__ == "__main__":
    from cheroot.wsgi import PathInfoDispatcher as WSGIPathInfoDispatcher
    from cheroot.wsgi import Server as WSGIServer
    my_app = WSGIPathInfoDispatcher({'/': app})
    server = WSGIServer(('0.0.0.0', int(os.environ.get('PORT',32729)) ), my_app)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
