from functools import wraps
import time
from collections import defaultdict
from typing import Callable, TextIO, Any
from dataclasses import dataclass
import sys

@dataclass
class _TimerLog:
    elapsed_time: float = 0.0
    count: int = 0
    def add(self, elapsed_time: float):
        self.elapsed_time += elapsed_time
        self.count += 1

class Timer:
    start_time: float = time.time()
    timer_logs = defaultdict(_TimerLog)
    @classmethod
    def measure(cls, func: Callable) -> Callable:
        """時間計測デコレータ

        Args:
            func (Callable): デコレータとして使う関数

        Returns:
            Callable: ラップ関数
        """
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            cls.timer_logs[func.__name__].add(end - start)
            return result
        return wrapper
    
    @classmethod
    def show(cls, file: TextIO=sys.stderr):
        """measureメソッドの計測結果をfileへ出力する

        Args:
            file (TextIO, optional): 結果を出力するファイル Defaults to sys.stderr.
        """
        for func, log in cls.timer_logs.items():
            print(f"function name       : {func}", file=file)
            print(f"called count        : {log.count}", file=file)
            print(f"sum of elapsed time : {log.elapsed_time:.4f}", file=file)
            print(f"", file=file)
    
    @classmethod
    def get_elapsed_time(cls) -> float:
        """Timerクラスの初期化からの経過時間を返す

        Returns:
            float: 経過時間
        """
        return time.time() - cls.start_time 
