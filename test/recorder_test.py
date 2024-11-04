from recorder import Recorder
import json

if __name__ == "__main__":
    Recorder.regist("time", 1)
    Recorder.regist("score", 1.23)
    data = Recorder.registed_data
    dumped_data = json.dumps(data)
    result = Recorder.get_registed_data(f"# @Recorder: {dumped_data}")
    print(data)
    print("result", result)
