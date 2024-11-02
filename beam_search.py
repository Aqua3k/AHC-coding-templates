from typing import Any, Generator
from heapq import heapify, heappushpop, heappush

Status = Any
Diff = Any
Score = int|float

class BeamSearchTemplate:
    def __init__(self, beam_width: int):
        self.depth = 0
        self.beam_width = beam_width

    def step(self, status: Status) -> Generator[list[tuple[Status, Score]], None, None]:
        pass

    def forward(self):
        pass

    def should_terminate(self) -> bool:
        pass

    def update_beam_width(self, beam_width) -> int:
        self.beam_width = beam_width

    def optimize(self, initial_status: Status, initial_score: Score) -> Status:
        def push(operation, score):
            if len(top_paths) < self.beam_width:
                heappush(top_paths, (score, operation))
            else:
                heappushpop(top_paths, (score, operation))

        paths: list[tuple[int, Status]] = [(initial_score, initial_status)]
        heapify(paths)
        while not self.should_terminate():
            top_paths: list[tuple[int, Status]] = []
            heapify(top_paths)
            for _, path in paths:
                for new_status, score in self.step(path):
                    push(new_status, score)
            paths = top_paths
            self.depth += 1
            self.forward()

        return path
