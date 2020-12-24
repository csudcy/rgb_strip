import io

import flask

app = flask.Flask(__name__)


@app.route('/')
def main():
  return flask.send_from_directory('.', 'index.html')


@app.route('/stream')
def stream():
  return flask.Response(display_thread_iterator(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


def display_thread_iterator():
  import time
  now = time.time()
  last_image = None
  while True:
    if last_image == DISPLAY_THREAD.image:
      # Wait for a bit
      time.sleep(0.001)
    else:
      # Show a new image
      last_image = DISPLAY_THREAD.image
      buffer = io.BytesIO()
      DISPLAY_THREAD.image.save(buffer, format='BMP')
      yield from (
          b'--frame\r\n',
          b'Content-Type: image/png\r\n',
          b'\r\n',
          buffer.getvalue(),
          b'\r\n',
      )


def run(display_thread):
  global DISPLAY_THREAD
  DISPLAY_THREAD = display_thread
  app.run()
