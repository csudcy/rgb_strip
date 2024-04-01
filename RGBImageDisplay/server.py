import io
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
  frame_info_dict = {
      'name': DISPLAY_THREAD.frame_info.name,
      'frames': DISPLAY_THREAD.frame_info.frames,
      'frame_index': DISPLAY_THREAD.frame_info.frame_index,
  }
  return flask.jsonify(frame_info_dict)


@app.route('/stream')
def stream():
  return flask.Response(display_thread_iterator(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/move_next')
def api_move_next():
  DISPLAY_THREAD.move_next = True
  return flask.jsonify({})


@app.route('/api/play')
def api_play():
  DISPLAY_THREAD.play_next = (flask.request.args['group'],
                              flask.request.args['image'])
  DISPLAY_THREAD.move_next = True
  return flask.jsonify({})


def display_thread_iterator():
  LOGGER.info('Serving new image iterator...')
  current_frame_info = None
  while True:
    if current_frame_info == DISPLAY_THREAD.frame_info:
      # Wait for a bit
      time.sleep(0.001)
    else:
      # Show a new image
      LOGGER.debug('Showing new image...')
      current_frame_info = DISPLAY_THREAD.frame_info
      buffer = io.BytesIO()
      current_frame_info.image.save(buffer, format='png')
      output = b'\r\n'.join((
          b'--frame',
          b'Content-Type: image/png',
          b'',
          buffer.getvalue(),
          b'',
      ))
      LOGGER.debug('Sending bytes...')
      yield output


def run(display_thread):
  global DISPLAY_THREAD
  DISPLAY_THREAD = display_thread
  app.run(host='0.0.0.0')
