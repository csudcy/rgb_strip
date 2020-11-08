# Think this has to be first
from gevent import monkey

monkey.patch_all()

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


@app.get('/ang')
def get_index_ang():
  return bottle.static_file('index_ang.html', root=HTML_DIRECTORY)


@app.get('/static/<filepath:path>')
def get_static(filepath):
  return bottle.static_file(filepath, root=STATIC_DIRECTORY)


@app.get('/ws')
def handle_websocket():
  """Open a websocket which will receive display updates.
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
      print(f'Unexpected message received: {message}')
    except WebSocketError as ex:
      print(f'WebSocketError: {str(ex)}')
      break
    finally:
      # Remove this from the list of websockets to send display updates to
      ws_display.remove_websocket(ws)


@app.get('/constants')
def get_constants():
  """Get any constants useful to the frontend e.g. list of display types.
  """
  import inspect

  from RGBStrip import constants, utils

  def get_args(klass_or_function, ignore=[]):
    if inspect.isclass(klass_or_function):
      klass_or_function = klass_or_function.__init__
    argspec = inspect.getfullargspec(klass_or_function)
    ignore.append('self')
    args = list(set(argspec.args) - set(ignore))
    args.sort()
    return args

  return {
      'config': {
          'palettes': get_args(utils.make_palette),
          'general': ['sleep_time'],
          'controllers': {
              key: get_args(klass)
              for key, klass in constants.CONTROLLERS.items()
          },
          'displays': {
              key: get_args(klass, ['controller'])
              for key, klass in constants.DISPLAYS.items()
          },
          'renderers': {
              key: get_args(klass, ['loader'])
              for key, klass in constants.RENDERERS.items()
          },
          'sections': {
              key: get_args(klass, ['controller'])
              for key, klass in constants.SECTIONS.items()
          },
      },
      'colours': list(constants.COLOURS.keys()),
  }


@app.get('/config')
def get_config():
  """Get the current config.
  """
  return MANAGER.get_yaml_config()


@app.post('/config')
def set_config():
  """Save the given config and start using it.
  """
  data = bottle.request.body.read()
  MANAGER.apply_config(data)


def start_server(manager, host='0.0.0.0', port=8080):
  """Start the server on http://{host}:{port} and return.
  """
  # TODO: Ewwww, globals :(
  global MANAGER
  MANAGER = manager

  # Construct & start the server
  server = WSGIServer((host, port), app, handler_class=WebSocketHandler)
  print(
      'NOTE: You must have a websocket display setup for display in browser to work!'
  )
  print(f'Starting server on {host}:{port}...')
  server.start()
