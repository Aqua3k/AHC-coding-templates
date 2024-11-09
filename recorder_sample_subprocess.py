"""recorderの使用例(子プロセスとして呼び出される側)

親プロセスに渡したいデータをRecorder.registで登録する
"""

import time

from timer import Timer
from recorder import Recorder

if __name__ == "__main__":
    Recorder.regist("score", 100)
    time.sleep(1)
    Recorder.regist("time", Timer.get_elapsed_time())
