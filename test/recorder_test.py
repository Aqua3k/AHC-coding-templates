import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from recorder import Recorder
import subprocess

if __name__ == "__main__":
    cmd = f"python test/subprocess_with_recorder.py"
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    data = Recorder.get_registed_data(proc.stderr)
    print(data)
