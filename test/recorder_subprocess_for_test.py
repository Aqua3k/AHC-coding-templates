from .. import recorder
import sys

if __name__ == "__main__":
    print("hello.")
    print("hello.", file=sys.stderr)
    recorder.Recorder.regist("time", 1)
    recorder.Recorder.regist("score", 1.23)
