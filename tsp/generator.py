import random
from typing import Hashable
from dataclasses import dataclass

@dataclass
class Tsp:
    size: int
    positions: list[tuple[int, int]]
    min_x: int
    max_x: int
    min_y: int
    max_y: int

def generate(
        seed: None|Hashable=None,
        size=100,
        min_x=-1000,
        max_x=1000,
        min_y=-1000, 
        max_y=1000,
        regenerate_dist=10,
        ):
    if seed is not None:
        random.seed(seed)

    positions = []
    while len(positions) < size:
        rand_x = random.randint(min_x, max_x)
        rand_y = random.randint(min_y, max_y)

        min_dist = float('inf')
        for x, y in positions:
            dist = (x - rand_x) ** 2 + (y - rand_y) ** 2
            min_dist = min(min_dist, dist)
        if min_dist <= regenerate_dist ** 2:
            continue # 近すぎるなら再生成

        positions.append([rand_x, rand_y])

    return Tsp(size, positions, min_x, max_x, min_y, max_y)
