import logging
import time

import flask

LOGGER = logging.getLogger(__name__)

app = flask.Flask(__name__)


@app.route('/')
def main():
  return flask.send_from_directory('.', 'index.html')


@app.route('/stream')
def stream():
  return flask.Response(display_thread_iterator(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


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
