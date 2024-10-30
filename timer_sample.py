"""Timerクラスの使用例

以下のように実行時間とコールされた回数がログ出力される
(デフォルトでは標準エラー出力に出力される)
```
function name       : sample_function1
called count        : 30
sum of elapsed time : 3.0070

function name       : sample_function2
called count        : 30
sum of elapsed time : 0.0000

```
"""

from timer import Timer
import time
import atexit

@Timer.measure
def sample_function1():
    time.sleep(0.1)

@Timer.measure
def sample_function2():
    # this function do nothing
    pass

if __name__ == "__main__":
    atexit.register(Timer.show)
    while Timer.get_elapsed_time() < 3:
        sample_function1()
        sample_function2()
