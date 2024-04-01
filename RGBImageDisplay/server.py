import io
import logging
import time

import flask

import devices
import rgb_image_display

LOGGER = logging.getLogger(__name__)

DISPLAY_THREAD = None
DEVICE = None

app = flask.Flask(__name__)


@app.route('/')
def main():
  context = {
      'width': DEVICE.width,
      'height': DEVICE.height,
      'rotate': DEVICE.rotate,
      'alpha': DEVICE.alpha,
      'delay_seconds': DISPLAY_THREAD.delay_seconds,
      'image_groups': DISPLAY_THREAD.image_groups,
  }
  return flask.render_template('index.tpl', **context)


@app.route('/frame_info')
def frame_info():
  frame_info_dict = {
      'parent': DISPLAY_THREAD.frame_info.image_info.parent,
      'name': DISPLAY_THREAD.frame_info.image_info.name,
      'frames': DISPLAY_THREAD.frame_info.image_info.n_frames,
      'frame_index': DISPLAY_THREAD.frame_info.frame_index,
  }
  return flask.jsonify(frame_info_dict)


@app.route('/stream')
def stream():
  return flask.Response(display_thread_iterator(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/move_next')
def api_move_next():
  DISPLAY_THREAD.next()
  return flask.jsonify({})


@app.route('/api/play')
def api_play():
  DISPLAY_THREAD.play(flask.request.args['group'], flask.request.args['image'])
  return flask.jsonify({})


def display_thread_iterator():
  LOGGER.info('Serving new image iterator...')
  current_image = None
  while True:
    if current_image == DISPLAY_THREAD.frame_info.image:
      # Wait for a bit
      time.sleep(0.001)
    else:
      # Show a new image
      LOGGER.debug('Showing new image...')
      current_image = DISPLAY_THREAD.frame_info.image
      buffer = io.BytesIO()
      current_image.save(buffer, format='png')
      output = b'\r\n'.join((
          b'--frame',
          b'Content-Type: image/png',
          b'',
          buffer.getvalue(),
          b'',
      ))
      LOGGER.debug('Sending bytes...')
      yield output


def run(device: devices.ImageDevice, display_thread: rgb_image_display.ImageDisplay):
  global DEVICE, DISPLAY_THREAD
  DEVICE = device
  DISPLAY_THREAD = display_thread
  app.run(host='0.0.0.0')
