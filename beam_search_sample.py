import atexit
from copy import deepcopy
from typing import Any

from beam_search import BeamSearchTemplate
from tsp.utility import Tsp, generate, visualize
from timer import Timer

class TourList:
    def __init__(self, tsp: Tsp):
        self.tsp = tsp
        self.tour_list: list[int] = [0]
        self.sum_of_dist: float = 0.0

    def get_dist(self, idx1: int, idx2: int) -> float:
        d = (self.tsp.positions[idx1][0] - self.tsp.positions[idx2][0]) ** 2\
            + (self.tsp.positions[idx1][1] - self.tsp.positions[idx2][1]) ** 2
        return pow(d, 0.5)

    def add(self, index: int):
        self.sum_of_dist += self.get_dist(self.tour_list[-1], index)
        self.tour_list.append(index)

    def __eq__(self, other: Any) -> bool:
        return True

    def __deepcopy__(self, _) -> 'TourList':
        replica = TourList(self.tsp)
        replica.tour_list = self.tour_list[:]
        replica.sum_of_dist = self.sum_of_dist
        return replica

class TspSolver(BeamSearchTemplate):
    def __init__(self, size: int) -> None:
        self.size = size
        super().__init__(1000)

    def step(self, status: TourList) -> None:
        for i in range(tsp.size):
            if i not in status.tour_list:
                s = deepcopy(status)
                s.add(i)
                self.add(-s.sum_of_dist, s)

    def should_terminate(self) -> bool:
        return self.size - 1 <= self.depth

if __name__ == "__main__":
    atexit.register(Timer.show)
    tsp = generate(size=10)
    status = TourList(tsp)
    solver = TspSolver(tsp.size)
    results = solver.optimize(status)
    visualize(tsp, results[0][1].tour_list)
