from typing import Any
from heapq import heapify, heappushpop, heappush
from abc import ABC, abstractmethod
import sys

Status = Any
Diff = Any
Score = int|float

class BeamSearchTemplate(ABC):
    def __init__(self, beam_width: int) -> None:
        """コンストラクタ

        Args:
            beam_width (int): ビームサーチ幅
        """
        self.depth = 0
        self.beam_width = beam_width
        self.top_paths: list[tuple[Score, Status]] = []

    @abstractmethod
    def step(self, status: Status) -> None:
        """次の状態を探す

        サブクラスで実装すること

        Args:
            status (Status): 現在の解の状態
        """
        pass

    def turn_elapsed(self) -> None:
        """1階層分経過したことを通知する

        必要あればオーバーライドすること
        """
        print(f"Turn {self.depth + 1} completed.", file=sys.stderr)

    @abstractmethod
    def should_terminate(self) -> bool:
        """探索を終了すべきか判断する

        サブクラスで実装すること

        Returns:
            bool: True: 探索終了 / False: 探索を続ける
        """
        pass

    def add(self, score: Score, status: Status) -> None:
        """次の状態を追加する

        stepもしくはturn_elapsedの中からコールすること

        Args:
            score (Score): スコア
            status (Status): 追加する解の状態
        """
        if len(self.top_paths) < self.beam_width:
            heappush(self.top_paths, (score, status))
        else:
            heappushpop(self.top_paths, (score, status))

    def update_beam_width(self, beam_width: int) -> None:
        """ビーム幅を更新する

        Args:
            beam_width (int): 更新するビーム幅
        """
        self.beam_width = beam_width

    def optimize(self, initial_status: Status) -> list[tuple[Score, Status]]:
        """ビームサーチを実行して解を求める

        Args:
            initial_status (Status): 初期状態

        Returns:
            list[tuple[Score, Status]]: ビームサーチで残ったスコアと状態のリスト
        """
        paths: list[tuple[Score, Status]] = [(0, initial_status)]
        heapify(paths)
        while not self.should_terminate():
            self.top_paths: list[tuple[Score, Status]] = []
            heapify(self.top_paths)
            for _, path in paths:
                self.step(path)
            paths = self.top_paths
            self.turn_elapsed()
            self.depth += 1

        return paths
