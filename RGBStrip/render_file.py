import itertools
import json
import os
from typing import Any, Iterable, Iterator, List, Tuple, Optional


class RenderWriter:

  def __init__(self, name: str, frames: Iterable[Any], frame_interval: int=0) -> None:
    if not name:
      raise Exception('Cannot render to memory without a name!')

    self.name = name
    self.frames = frames
    self.frame_interval = frame_interval

  def write(self, directory: str) -> None:
    # Save the frames
    print(f'{self.name}: Writing data file...')
    frame_lengths = []
    framedata_path = os.path.join(directory, f'{self.name}.data')
    with open(framedata_path, 'wb') as f:
      for frame_count, frame in enumerate(self.frames):
        if frame_count % 100 == 0:
          print(f'{self.name}: Saved {frame_count} frames...')
        frame_dumped = bytes(self.dump_frame(frame))
        frame_lengths.append(len(frame_dumped))
        f.write(frame_dumped)
    print(f'{self.name}: Saved {frame_count} frames')

    unique_frame_lengths = set(frame_lengths)
    if len(list(unique_frame_lengths)) != 1:
      raise Exception(f'Got frames of multiple lengths: {unique_frame_lengths}')

    # Save the meta JSON file
    print(f'{self.name}: Writing JSON file...')
    render_data = {
        'frame_count': len(frame_lengths),
        'frame_length': frame_lengths[0],
        'frame_interval': self.frame_interval,
    }
    with open(os.path.join(directory, f'{self.name}.json'), 'w') as f:
      json.dump(render_data, f, indent=2, sort_keys=True)
    print(f'{self.name}: Done!')

  def dump_frame(self, frame: List[Tuple[int, int, int]]) -> Iterator[int]:
    for r, g, b in frame:
      yield r
      yield g
      yield b


class RenderReader:

  def __init__(self, name: str, frame_interval: int, frame_count: int, frame_length: int, framedata_path: str) -> None:
    self.name = name
    self.frame_interval = frame_interval
    self.frame_count = frame_count
    self.frame_length = frame_length
    self.framedata_path = framedata_path

  @classmethod
  def load(cls, directory: str, name: str) -> Optional['cls']:
    # Load the renderer
    with open(os.path.join(directory, f'{name}.json'), 'r') as f:
      render = json.load(f)

    return cls(
        name=name,
        frame_interval=render['frame_interval'],
        frame_count=render['frame_count'],
        frame_length=render['frame_length'],
        framedata_path=os.path.join(directory, f'{name}.data'),
    )

  @property
  def frames(self) -> Iterator[Any]:
    # Open the data file & iterate over the frames
    with open(self.framedata_path, 'rb') as framedata_file:
      for frame_index in range(self.frame_count):
        if frame_index % 100 == 0:
          print(f'Frame {frame_index} / {self.frame_count}')

        # Load the next frame & send it to controller
        framedata = framedata_file.read(self.frame_length)
        yield self.load_frame(framedata)

  def load_frame(self, data: bytes) -> List[Tuple[int, int, int]]:
    pixels = [iter(data)] * 3
    return [
        (int(r), int(g), int(b))
        for r, g, b in itertools.zip_longest(*pixels)
    ]
