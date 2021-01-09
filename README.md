# Deprecated
This project was discontinued due to internal structural problems. Please check
[lemon-mint/event-broker](https://github.com/lemon-mint/event-broker)

# flask-event-server
flask-event-server
Is minimal and unoptimized
Server-Sent Events Server

### stable
[![buildstate](https://github.com/lemon-mint/flask-event-server/workflows/build-latest/badge.svg)](https://hub.docker.com/r/icelemonmint/flask-event-server)

### dev version
[![build-dev-latest](https://github.com/lemon-mint/flask-event-server/workflows/build-dev-latest/badge.svg?branch=master)](https://hub.docker.com/r/icelemonmint/flask-event-server-dev)

# APIS
## /sse/listen/\<sha384 hash of channel name\>
example code
``` javascript
function makeconn() {
    var evt = new EventSource('/sse/listen/cf2daa804389e2eedd4fdc41e32e1f481a5ec493b956ece1d4d0fa2427188636bfe0b1abc462677e54b1d8d7447bc494');
    evt.addEventListener('open', function (e) {
        console.log('connected');
    }, false);
    evt.addEventListener('myevent', function (e) {
        console.log(e);
    }, false);
    evt.addEventListener('error', function (e) {
        evt.close();
        makeconn();
    }, false);
}
makeconn();
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
