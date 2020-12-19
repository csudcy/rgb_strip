import os
import pickle
import shutil
from typing import Any, Iterable, Iterator, List, Optional


class RenderWriter:

  def __init__(self, name: str, frames: Iterable[Any], frame_interval: int=0) -> None:
    if not name:
      raise Exception('Cannot render to memory without a name!')

    self.name = name
    self.frames = frames
    self.frame_interval = frame_interval

  def write(self, directory: str) -> None:
    print(f'{self.name}: Rendering...')

    # Make sure the output directory exists & is clear
    render_directory = os.path.join(directory, self.name)
    if os.path.exists(render_directory):
      print(f'{self.name}: Removing directory...')
      shutil.rmtree(render_directory)
    print(f'{self.name}: Adding directory...')
    os.makedirs(render_directory)

    # Save the frames
    frame_lengths = []
    framedata_path = os.path.join(render_directory, f'data.pickle')
    with open(framedata_path, 'wb') as f:
      for frame_count, frame in enumerate(self.frames):
        if frame_count % 100 == 0:
          print(f'{self.name}: Saved {frame_count} frames...')
        frame_dumped = pickle.dumps(frame)
        frame_lengths.append(len(frame_dumped))
        f.write(frame_dumped)
    print(f'{self.name}: Saved {frame_count} frames')

    # Save the init.pickle file
    render_data = {
        'name': self.name,
        'frame_lengths': frame_lengths,
        'frame_interval': self.frame_interval,
    }
    print(f'{self.name}: Writing init.pickle...')
    with open(os.path.join(render_directory, f'init.pickle'), 'wb') as f:
      pickle.dump(render_data, f)
    print(f'{self.name}: Done!')


class RenderReader:

  def __init__(self, name: str, frame_interval: int, frame_lengths: List[int], framedata_path: str) -> None:
    self.name = name
    self.frame_interval = frame_interval
    self.frame_lengths = frame_lengths
    self.frame_count = len(frame_lengths)
    self.framedata_path = framedata_path

  @classmethod
  def load(cls, directory: str) -> Optional['cls']:
    # Check this really is a render
    init_filepath = os.path.join(directory, 'init.pickle')
    if not os.path.exists(init_filepath):
      return

    # Load the renderer
    with open(init_filepath, 'rb') as f:
      render = pickle.load(f)

    return cls(
        name=render['name'],
        frame_interval=render['frame_interval'],
        frame_lengths=render['frame_lengths'],
        framedata_path=os.path.join(directory, 'data.pickle'),
    )

  @property
  def frames(self) -> Iterator[Any]:
    # Open the data file & iterate over the frames
    with open(self.framedata_path, 'rb') as framedata_file:
      for frame_index, frame_length in enumerate(self.frame_lengths):
        if frame_index % 100 == 0:
          print(f'Frame {frame_index} / {self.frame_count}')

        # Load the next frame & send it to controller
        framedata = framedata_file.read(frame_length)
        frame = pickle.loads(framedata)
        yield frame
