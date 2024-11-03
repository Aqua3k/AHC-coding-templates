import sys
import json
import atexit
import re

JSONType = None |\
        bool |\
        int |\
        float |\
        str|\
        list['JSONType'] |\
        dict[str, 'JSONType']
ValueName = str
RegistedData = dict[ValueName, JSONType]

class Recorder:
    initial_regist = True
    registed_data: dict[ValueName, JSONType] = dict()
    @classmethod
    def regist(cls, value_name: ValueName, data: JSONType):
        if cls.initial_regist:
            atexit.register(cls.finalize)
            cls.initial_regist = False
        cls.registed_data[value_name] = data
    
    @classmethod
    def finalize(cls):
        damped_data = json.dumps(cls.registed_data)
        print(f"# @Recorder: {damped_data}", file=sys.stderr)
    
    @staticmethod
    def get_registed_data(stderr: str|None) -> RegistedData:
        if stderr is None:
            return dict()
        match = re.match(r'# @Recorder: (\{.*\})', stderr)
        if match:
            registed_data = match.group(1)
            return json.loads(registed_data)
        return dict()
