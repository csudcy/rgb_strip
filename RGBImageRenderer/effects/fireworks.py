import collections
from dataclasses import dataclass
import math
import random
from typing import Deque, Generator, List, Optional, Tuple

from PIL import Image
from PIL import ImageDraw

import colours
from effects import base


class Particle:

  def __init__(
      self,
      *,
      g_speed: float,
      width: int,
      height: int,
      colour: colours.ColourType,
      x: float,
      y: float,
      angle: float,
      speed: float,
      add_dx: float = 0,
      add_dy: float = 0,
      trail_distance: int = 2,
      lifetime: int = 99999,
  ):
    self.width = width
    self.height = height
    self.dx = math.sin(math.radians(angle)) * speed + add_dx
    self.dy = math.cos(math.radians(angle)) * speed + add_dy
    self.g_speed = g_speed
    self.lifetime = lifetime

    self.point_count = trail_distance + 1
    self.colours = [(
        int(colour[0] * i / (self.point_count + 1)),
        int(colour[1] * i / (self.point_count + 1)),
        int(colour[2] * i / (self.point_count + 1)),
    ) for i in range(self.point_count + 1, 1, -1)]
    self.points = [(x, y)]

  def draw(self, canvas: ImageDraw.Draw) -> None:
    # Draw my points
    for (x, y), colour in zip(self.points, self.colours):
      canvas.point((int(x) % self.width, int(self.height - y)), colour)

    # Update position/speed/lifetime
    x, y = self.points[0]
    self.points.insert(0, (x + self.dx, y + self.dy))
    self.points = self.points[:self.point_count]
    self.dy -= self.g_speed
    self.lifetime -= 1

  @property
  def done(self) -> bool:
    return self.lifetime < 0 or all(y < 0 for x, y in self.points)

  @property
  def colour(self) -> colours.ColourType:
    return self.colours[0]

  @property
  def x(self) -> float:
    return self.points[0][0]

  @property
  def y(self) -> float:
    return self.points[0][1]


class FireworksEffect(base.BaseEffect):

  def __init__(
      self,
      width: int,
      height: int,
      name: str,
      palette: List[colours.ColourType],
      # Custom
      g_speed: float = 0.1,
      # Shots
      shots_max: int = 10,  # Maximum number of shots on screen at once
      shot_add_chance: float = 0.17,  # Chance of adding another shot
      shot_speed: Tuple[float, float] = (3.0, 5.0),
      shot_angle: Tuple[float, float] = (-20.0, 20.0),
      # Explosions
      explosion_count: Tuple[int, int] = (10, 20),
      explosion_speed: Tuple[float, float] = (1.0, 3.0),
      explosion_lifetime: Tuple[int, int] = (10, 13),
  ):
    super().__init__(width, height, name, palette)
    self.g_speed = g_speed
    # Shots
    self.shots_max = shots_max
    self.shot_add_chance = shot_add_chance
    self.shot_speed = shot_speed
    self.shot_angle = shot_angle
    # Explosions
    self.explosion_count = explosion_count
    self.explosion_speed = explosion_speed
    self.explosion_lifetime = explosion_lifetime

  def iter_images(self) -> Generator[Image.Image, None, None]:
    shot_particles = []
    explosion_particles = []

    for i in range(1000):
      image, canvas = self.get_blank_image()

      # Remove old explosions
      explosion_particles = [
          explosion_particle for explosion_particle in explosion_particles
          if not explosion_particle.done
      ]

      # Remove old shots & explode them
      for shot_particle in shot_particles:
        if shot_particle.dy < 0.1:
          shot_particles.remove(shot_particle)
          explosion_particles += [
              Particle(
                  g_speed=self.g_speed,
                  width=self.width,
                  height=self.height,
                  colour=shot_particle.colour,
                  x=shot_particle.x,
                  y=shot_particle.y,
                  add_dx=shot_particle.dx,
                  add_dy=shot_particle.dy,
                  angle=random.uniform(0, 360),
                  speed=random.uniform(*self.explosion_speed),
                  lifetime=random.randint(*self.explosion_lifetime),
              ) for i in range(random.randint(*self.explosion_count))
          ]

      # Add a new shot (maybe)
      if len(shot_particles) < self.shots_max:
        if random.random() < self.shot_add_chance:
          shot_particles.append(
              Particle(
                  g_speed=self.g_speed,
                  width=self.width,
                  height=self.height,
                  colour=random.choice(self.palette),
                  x=random.randint(0, self.width),
                  y=0,
                  angle=random.uniform(*self.shot_angle),
                  speed=random.uniform(*self.shot_speed),
              ))

      # Show all the particles
      for shot_particle in shot_particles:
        shot_particle.draw(canvas)
      for explosion_particle in explosion_particles:
        explosion_particle.draw(canvas)

      yield image
