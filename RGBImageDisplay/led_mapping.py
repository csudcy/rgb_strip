from typing import List


def make_snake(width: int, height: int, flip_x: bool,
               flip_y: bool) -> List[int]:
  """Make an LED mapping
  Given LEDs arranged like this:
    0  7  8
    1  6  9
    2  5  10
    3  4  11

  Map them to positions expected like this:
    0  1  2
    3  4  5
    6  7  8
    9  10 11

  Return an array like this:
    [0, 7, 8, 1, 6, 9, 2, 5, 10, 3, 4, 11]
  """
  mapping = []
  for j in range(height):
    for i in range(width):
      if flip_x:
        x = width - 1 - i
      else:
        x = i

      if flip_y:
        y = height - 1 - j
      else:
        y = j

      if i % 2 == 0:
        index = x * height + y
      else:
        index = x * height + (height - y - 1)
      mapping.append(index)
  return mapping


if __name__ == '__main__':
  TESTS = (
      # 0  7  8
      # 1  6  9
      # 2  5  10
      # 3  4  11
      (False, False, [0, 7, 8, 1, 6, 9, 2, 5, 10, 3, 4, 11]),
      # 3  4  11
      # 2  5  10
      # 1  6  9
      # 0  7  8
      (False, True, [3, 4, 11, 2, 5, 10, 1, 6, 9, 0, 7, 8]),
      # 8  7  0
      # 9  6  1
      # 10 5  2
      # 11 4  3
      (True, False, [8, 7, 0, 9, 6, 1, 10, 5, 2, 11, 4, 3]),
      # 11 4  3
      # 10 5  2
      # 9  6  1
      # 8  7  0
      (True, True, [11, 4, 3, 10, 5, 2, 9, 6, 1, 8, 7, 0]),
  )
  for index, (flip_x, flip_y, expected_result) in enumerate(TESTS):
    result = make_snake(3, 4, flip_x, flip_y)
    if result == expected_result:
      print(f'{index}. PASS')
    else:
      print(f'{index}. FAIL')
      print(f'  Expected: {expected_result}')
      print(f'  Actual  : {result}')
