import random
import math
from copy import deepcopy
from typing import Any

Status = Any
Score = int|float

class DiffRecord:
    pass

class SimulatedaAnnealingTemplate:
    def should_terminate(self) -> bool:
        pass

    def get_evaluated_value(self, status: Status) -> Score:
        pass

    def solve(self, initial_status: Status, temperture: int|float, rate: float) -> Status:
        score = self.get_evaluated_value(initial_status)
        best_score = score

        status = initial_status
        best_status = initial_status

        while not self.should_terminate():
            diff, new_score = self.dry_run(status, score)
            t = (score - new_score) / temperture
            if t >= 1.0:
                swap = True
            else:
                swap = random.random() < pow(math.e, t)

            if swap:
                status = self.operate(status, diff)
                score = new_score
                if score < best_score:
                    best_score = score
                    best_status = deepcopy(status)
            
            temperture *= rate
        
        return best_status

    def dry_run(self, status: Status, score: Score) -> tuple[DiffRecord, Score]:
        pass

    def operate(self, status: Status, diff: DiffRecord) -> Status:
        pass

