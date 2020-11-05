# flask-event-server
flask-event-server
Is minimal and unoptimized
EventSource server side event server

### stable
[![buildstate](https://github.com/lemon-mint/flask-event-server/workflows/build-latest/badge.svg)](https://hub.docker.com/r/icelemonmint/flask-event-server)

# APIS
## /sse/listen/\<sha384 hash of channel name\>
example code
``` javascript
var evt = new EventSource('/sse/listen/cf2daa804389e2eedd4fdc41e32e1f481a5ec493b956ece1d4d0fa2427188636bfe0b1abc462677e54b1d8d7447bc494');
evt.addEventListener('open', function(e) {
    console.log('connection opened');
}, false);
evt.addEventListener('myevent', function(e) {
    console.log(e);
}, false);
evt.addEventListener('error', function(e) {
    if (e.eventPhase == EventSource.CLOSED) {
        console.log('connection closed');
    }
}, false);
```
## /sse/deploy/\<channel name\>
```
GET /sse/deploy/mychannel?type=myevent&sub=1000

{"eventid":"ab7dca31b9dea1bebf5e","sub":1000,"success":true,"time":1604566637.6499722}
```
## /calc/\<channel name\>
Calculate the sha384 value of the channel name.
```
GET /calc/mychannel

cf2daa804389e2eedd4fdc41e32e1f481a5ec493b956ece1d4d0fa2427188636bfe0b1abc462677e54b1d8d7447bc494
```
