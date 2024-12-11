from typing import Any
from heapq import heapify, heappushpop, heappush

Status = Any
Diff = Any
Score = int|float

class BeamSearchTemplate:
    def __init__(self, beam_width: int):
        self.depth = 0
        self.beam_width = beam_width

    def step(self, status: Status) -> None:
        pass

    def forward(self) -> None:
        pass

    def should_terminate(self) -> bool:
        pass

    def add(self, score: Score, status: Status) -> None:
        if len(self.top_paths) < self.beam_width:
            heappush(self.top_paths, (score, status))
        else:
            heappushpop(self.top_paths, (score, status))

    def update_beam_width(self, beam_width: int) -> None:
        self.beam_width = beam_width

    def optimize(self, initial_status: Status) -> list[tuple[Score, Status]]:
        paths: list[tuple[Score, Status]] = [(0, initial_status)]
        heapify(paths)
        while not self.should_terminate():
            self.top_paths: list[tuple[int, Status]] = []
            heapify(self.top_paths)
            for _, path in paths:
                self.step(path)
            paths = self.top_paths
            self.forward()
            self.depth += 1

        return path
