from dataclasses import dataclass
import random
import atexit

from simulateda_annealing import SimulatedaAnnealingTemplate
from tsp.utility import Tsp, generate, visualize
from timer import Timer

def _get_dist(tsp: Tsp, idx1: int, idx2: int):
    d = (tsp.positions[idx1][0] - tsp.positions[idx2][0]) ** 2\
        + (tsp.positions[idx1][1] - tsp.positions[idx2][1]) ** 2
    return pow(d, 0.5)

TourList = list[int]

@dataclass
class TspDiff:
    swapped1: int
    swapped2: int

class TspSolver(SimulatedaAnnealingTemplate):
    def __init__(self, tsp: Tsp, timelimit: int=10):
        self.timelimit = timelimit
        self.tsp = tsp
        initial_tour_list = [i for i in range(self.tsp.size)]
        initial_score = self._get_sum_of_dist(initial_tour_list)
        super().__init__(initial_tour_list, initial_score)

    def _get_sum_of_dist(self, tour_list: TourList) -> float:
        sum_of_dist = 0
        for i in range(tsp.size - 1):
            sum_of_dist += _get_dist(self.tsp, tour_list[i], tour_list[i+1])
        sum_of_dist += _get_dist(self.tsp, tour_list[0], tour_list[-1])
        return sum_of_dist

    def should_terminate(self) -> bool:
        return self.timelimit < Timer.get_elapsed_time()

    @Timer.measure
    def dry_run(self, tour_list: TourList, sum_of_dist: float) -> tuple[TspDiff, float]:
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
        return TspDiff(idx1, idx2), sum_of_dist - dist_pre + dist_aft

    @Timer.measure
    def operate(self, tour_list: TourList, diff: TspDiff) -> TourList:
        x, y = diff.swapped1 + 1, diff.swapped2
        while x < y:
            tour_list[x],tour_list[y] = tour_list[y], tour_list[x]
            x += 1
            y -= 1
        return tour_list

if __name__ == "__main__":
    atexit.register(Timer.show)
    tsp = generate()
    solver = TspSolver(tsp)
    result = solver.optimize(100, 0.999)
    visualize(tsp, result)
