# Think this has to be first
from gevent import monkey; monkey.patch_all()

import os

import bottle
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

from RGBStrip.displays import websocket as ws_display

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
STATIC_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'static')
HTML_DIRECTORY = os.path.join(STATIC_DIRECTORY, 'html')

app = bottle.Bottle()


# TODO: Cache this!
def load_template(path):
    path = os.path.join(HTML_DIRECTORY, path) + '.html'
    with open(path, 'r') as f:
        contents = f.read()
    return bottle.SimpleTemplate(contents)


def render_template(path, context=None):
    template = load_template(path)
    return template.render(**(context or {}))


@app.get('/')
def get_index():
    return render_template('index')


@app.get('/static/<filepath:path>')
def get_static(filepath):
    return bottle.static_file(filepath, root=STATIC_DIRECTORY)


@app.get('/ws')
def handle_websocket():
    """
    Open a websocket which will receive display updates.
    """
    ws = bottle.request.environ.get('wsgi.websocket')
    if not ws:
        bottle.abort(400, 'Expected WebSocket request.')
        return

    # Add this socket to the list of listeners
    ws_display.add_websocket(ws)

    # Wait until the websocket is closed
    while True:
        try:
            message = ws.receive()
            print 'Unexpected message received: %s' % message
        except WebSocketError as ex:
            print 'WebSocketError: %s' % str(ex)
            break
        finally:
            # Remove this from the list of websockets to send display updates to
            ws_display.remove_websocket(ws)


@app.get('/constants')
def get_constants():
    """
    Get any constants useful to the frontend e.g. list of display types
    """
    import inspect

    from RGBStrip import constants, controller, section

    def get_args(klass, ignore=[]):
        argspec = inspect.getargspec(klass.__init__)
        args = list(set(argspec.args) - set(ignore))
        args.sort()
        return args

    return {
        'controller': get_args(controller.RGBStripController, ['self']),
        'section': get_args(section.SectionController, ['self', 'controller']),
        'displays': {
            key: get_args(klass, ['self', 'controller'])
            for key, klass in constants.DISPLAYS.iteritems()
        },
        'renderers': {
            key: get_args(klass, ['self', 'controllers'])
            for key, klass in constants.RENDERERS.iteritems()
        },
        'general': [
            'sleep_time'
        ]
    }


@app.get('/config')
def get_config():
    """
    Get the current config
    """
    return MANAGER.YAML_CONFIG


@app.post('/config')
def set_config():
    """
    Save the given config and start using it
    """
    data = bottle.request.body.read()
    MANAGER.apply_config(data)


def start_server(manager, host='0.0.0.0', port=8080):
    """
    Start the server on http://{host}:{port} and return
    """
    # TODO: Ewwww, globals :(
    global MANAGER
    MANAGER = manager

    # Construct & start the server
    server = WSGIServer(
        (host, port),
        app,
        handler_class=WebSocketHandler
    )
    print 'Starting server on {host}:{port}...'.format(
        host=host,
        port=port
    )
    server.start()
