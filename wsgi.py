from app import app as application

if __name__ == "__main__":
    from cheroot.wsgi import PathInfoDispatcher as WSGIPathInfoDispatcher
    from cheroot.wsgi import Server as WSGIServer
    my_app = WSGIPathInfoDispatcher({'/': app})
    server = WSGIServer(('0.0.0.0', int(os.environ.get('PORT',32729)) ), my_app)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
