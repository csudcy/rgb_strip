import logging
import time

import flask

LOGGER = logging.getLogger(__name__)

DISPLAY_THREAD = None

app = flask.Flask(__name__)


@app.route('/')
def main():
  context = {
      'width': DISPLAY_THREAD.width,
      'height': DISPLAY_THREAD.height,
      'rotate': DISPLAY_THREAD.rotate,
      'alpha': DISPLAY_THREAD.alpha,
      'delay_seconds': DISPLAY_THREAD.delay_seconds,
      'image_groups': DISPLAY_THREAD.image_groups,
  }
  return flask.render_template('index.tpl', **context)


@app.route('/frame_info')
def frame_info():
  return flask.jsonify(DISPLAY_THREAD.frame_info)


@app.route('/stream')
def stream():
  return flask.Response(display_thread_iterator(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/move_next')
def api_move_next():
  DISPLAY_THREAD.move_next = True
  return flask.jsonify(DISPLAY_THREAD.frame_info)


def display_thread_iterator():
  LOGGER.info('Serving new image iterator...')
  current_image_bytes = None
  while True:
    if current_image_bytes == DISPLAY_THREAD.image_bytes:
      # Wait for a bit
      time.sleep(0.001)
    else:
      # Show a new image
      LOGGER.debug('Showing new image...')
      current_image_bytes = DISPLAY_THREAD.image_bytes
      output = b'\r\n'.join((
          b'--frame',
          b'Content-Type: image/png',
          b'',
          current_image_bytes,
          b'',
      ))
      LOGGER.debug('Sending bytes...')
      yield output


def run(display_thread):
  global DISPLAY_THREAD
  DISPLAY_THREAD = display_thread
  app.run(host='0.0.0.0')
