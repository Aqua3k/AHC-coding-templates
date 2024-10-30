import random
import math
from copy import deepcopy

class DiffRecord:
    pass

class Problem:
    pass

class SimulatedaAnnealingTemplate:
    def __init__(self):
        pass

    def should_terminate(self) -> bool:
        pass

    def get_evaluated_value(self) -> int:
        pass

    def solve(self, initial_status: Problem, temperture: int|float, rate: float) -> Problem:
        score = self.get_evaluated_value()
        best_score = score

        status = initial_status
        best_status = initial_status

        while not self.should_terminate():
            diff, new_status, new_score = self.operate(status)
            t = (score - new_score) / temperture
            if t >= 1.0:
                swap = True
            else:
                swap = random.random() < pow(math.e, t)

            if swap:
                score = new_score
                status = new_status
                if score < best_score:
                    best_score = score
                    best_status = deepcopy(status)
            else:
                status = self.revert(new_status, diff)
            
            temperture *= rate
        
        return best_status

    def operate(self, problem: Problem) -> tuple[DiffRecord, Problem, int]:
        pass

    def revert(self, problem: Problem, diff: DiffRecord) -> Problem:
        pass

