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
