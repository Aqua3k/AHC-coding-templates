"""recorderの使用例(親プロセス側)

Recorder.registを使う子プロセスを実行する
子プロセスの標準エラー出力をRecorder.get_registed_dataに渡す
"""

import subprocess

from recorder import Recorder

if __name__ == "__main__":
    cmd = f"python recorder_sample_subprocess.py"
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    data = Recorder.get_registed_data(proc.stderr)
    print(data)
