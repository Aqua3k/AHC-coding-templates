import random
from typing import Hashable
from dataclasses import dataclass

import matplotlib.pyplot as plt

@dataclass
class Tsp:
    """TSP問題のデータクラス
    """
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
    """TSP問題をランダムに生成する

    Args:
        seed (None | Hashable, optional): シード値 Noneの場合はランダム Defaults to None.
        size (int, optional): TSPの都市サイズ Defaults to 100.
        min_x (int, optional): x座標の最小値 Defaults to -1000.
        max_x (int, optional): x座標の最大値 Defaults to 1000.
        min_y (int, optional): y座標の最小値 Defaults to -1000.
        max_y (int, optional): y座標の最大値 Defaults to 1000.
        regenerate_dist (int, optional): この値以下の距離の都市が生成されたら都市を再生成する Defaults to 10.

    Returns:
        _type_: _description_
    """
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

def visualize(tsp: Tsp, tour_list: list[int]):
    """TSP問題の解を図示する

    Args:
        tsp (Tsp): TSP問題
        tour_list (list[int]): TSP問題の解(訪問する都市の順番)
    """
    assert tsp.size == len(tour_list)

    x, y = [], []
    for a,b in tsp.positions:
        x.append(a)
        y.append(b)

    pre = tsp.positions[tour_list[0]]
    for idx in tour_list[1:]:
        a,b = tsp.positions[idx]
        plt.plot([pre[0], a], [pre[1], b], c="b", lw = 1)
        pre = [a,b]
    # 最後に0に戻る
    a,b = tsp.positions[0]
    plt.plot([pre[0], a], [pre[1], b], c="b", lw = 1)

    plt.scatter(x, y, s = 5, c = "k")
    plt.xlim(tsp.min_x, tsp.max_x)
    plt.ylim(tsp.min_y, tsp.max_y)

    plt.show()
