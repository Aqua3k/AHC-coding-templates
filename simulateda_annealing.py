import random
import math
from copy import deepcopy
from typing import Any

Status = Any
Diff = Any
Score = int|float

class SimulatedaAnnealingTemplate:
    def __init__(self, initial_status: Status, initial_score: Score):
        self.initial_status = initial_status
        self.initial_score = initial_score

    def should_terminate(self) -> bool:
        pass

    def optimize(self, temperature: int|float, rate: float) -> Status:
        score = self.initial_score
        best_score = score

        status = self.initial_status
        best_status = status

        while not self.should_terminate():
            diff, new_score = self.dry_run(status, score)
            t = (score - new_score) / temperature
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
            
            temperature *= rate
        
        return best_status

    def dry_run(self, status: Status, score: Score) -> tuple[Diff, Score]:
        pass

    def operate(self, status: Status, diff: Diff) -> Status:
        pass

