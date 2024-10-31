#TODO 正しく動くか確認する

import random
import math
from copy import deepcopy
from typing import Any

Status = Any

class DiffRecord:
    pass

class SimulatedaAnnealingTemplate:
    def __init__(self):
        pass

    def should_terminate(self) -> bool:
        pass

    def get_evaluated_value(self) -> int:
        pass

    def solve(self, initial_status: Status, temperture: int|float, rate: float) -> Status:
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

    def operate(self, status: Status) -> tuple[DiffRecord, Status, int]:
        pass

    def revert(self, status: Status, diff: DiffRecord) -> Status:
        pass

