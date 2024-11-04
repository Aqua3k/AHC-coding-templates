from .. import recorder
import json

if __name__ == "__main__":
    recorder.Recorder.regist("time", 1)
    recorder.Recorder.regist("score", 1.23)
    data = recorder.Recorder.registed_data
    dumped_data = json.dumps(data)
    result = recorder.Recorder.get_registed_data(f"# @recorder.Recorder: {dumped_data}")
    print(data)
    print("result", result)
