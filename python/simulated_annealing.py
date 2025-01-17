import random
import math
from copy import deepcopy
from typing import Any
from abc import ABC, abstractmethod

Status = Any
Diff = Any
Score = int|float

class SimulatedaAnnealingTemplate(ABC):
    def __init__(self, initial_status: Status, initial_score: Score) -> None:
        """コンストラクタ

        Args:
            initial_status (Status): 解の初期状態
            initial_score (Score): 初期解の評価値
        """
        self.initial_status = initial_status
        self.initial_score = initial_score

    @abstractmethod
    def should_terminate(self) -> bool:
        """焼きまなしを終了するか判定する

        焼きなましの各ループでコールされる
        サブクラスで実装すること

        Returns:
            bool: True(終了)/False(続行)
        """
        pass

    def optimize(self, temperature: int|float, rate: float) -> Status:
        """焼きなましを実行して解を求める

        Args:
            temperature (int | float): 温度
            rate (float): 温度を下げる割合、毎ループ温度に乗算される

        Returns:
            Status: 見つかった解
        """
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

    @abstractmethod
    def dry_run(self, status: Status, score: Score) -> tuple[Diff, Score]:
        """何かの操作を仮実行した場合の評価を行う

        サブクラスで実装すること

        Args:
            status (Status): 現在の解の状態
            score (Score): 現在のスコア

        Returns:
            tuple[Diff, Score]: 差分情報, 操作を実行した場合のスコア
        """
        pass

    @abstractmethod
    def operate(self, status: Status, diff: Diff) -> Status:
        """実際にDiffに対する操作を行う

        サブクラスで実装すること

        Args:
            status (Status): 現在の解の状態
            diff (Diff): 差分情報(dry_runで作ったやつ)

        Returns:
            Status: 操作後の解の状態
        """
        pass
