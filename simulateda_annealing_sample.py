from dataclasses import dataclass
import random

from simulateda_annealing import SimulatedaAnnealingTemplate, DiffRecord
from tsp.generator import Tsp, generate
from tsp.visualizer import visualize
from timer import Timer

def _get_dist(tsp: Tsp, idx1: int, idx2: int):
    d = (tsp.positions[idx1][0] - tsp.positions[idx2][0]) ** 2\
        + (tsp.positions[idx1][1] - tsp.positions[idx2][1]) ** 2
    return pow(d, 0.5)

TourList = list[int]

@dataclass
class _TspDiffRecord(DiffRecord):
    swapped1: int
    swapped2: int

class TspSolver(SimulatedaAnnealingTemplate):
    def __init__(self, tsp: Tsp, timelimit: int=10):
        self.timelimit = timelimit
        self.tsp = tsp

    def get_evaluated_value(self, tour_list):
        sum_of_dist = 0
        for i in range(tsp.size - 1):
            sum_of_dist += _get_dist(self.tsp, tour_list[i], tour_list[i+1])
        sum_of_dist += _get_dist(self.tsp, tour_list[0], tour_list[-1])
        return sum_of_dist

    def should_terminate(self) -> bool:
        return self.timelimit < Timer.get_elapsed_time()

    def dry_run(self, tour_list: TourList, sum_of_dist: float) -> tuple[DiffRecord, float]:
        idx1 = random.randint(0, self.tsp.size - 1)
        idx2 = random.randint(0, self.tsp.size - 2)
        if idx1 <= idx2:
            idx2 += 1
        if idx2 < idx1:
            idx1, idx2 = idx2, idx1

        dist_pre = _get_dist(self.tsp, tour_list[idx1], tour_list[idx1+1])\
             + _get_dist(self.tsp, tour_list[idx2], tour_list[(idx2+1)%tsp.size])
        dist_aft = _get_dist(self.tsp, tour_list[idx1], tour_list[idx2])\
             + _get_dist(self.tsp, tour_list[idx1+1], tour_list[(idx2+1)%tsp.size])
        return _TspDiffRecord(idx1, idx2), sum_of_dist - dist_pre + dist_aft

    def operate(self, tour_list: TourList, diff: _TspDiffRecord) -> TourList:
        x, y = diff.swapped1 + 1, diff.swapped2
        while x < y:
            tour_list[x],tour_list[y] = tour_list[y], tour_list[x]
            x += 1
            y -= 1
        return tour_list

if __name__ == "__main__":
    tsp = generate()
    solver = TspSolver(tsp)
    initial_tour_list = [i for i in range(tsp.size)]
    result = solver.solve(initial_tour_list, 100, 0.999)
    visualize(tsp, result)