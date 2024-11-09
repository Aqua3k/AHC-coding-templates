"""標準エラー出力を使って別プロセス間でデータをやり取りする仕組みを提供する
"""

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
    def __new__(cls, *args, **kwargs):
        # インスタンス化するとエラーにする
        raise TypeError(f"{cls.__name__} cannot be instantiated")

    @classmethod
    def regist(cls, value_name: ValueName, data: JSONType):
        """データを登録する

        Args:
            value_name (ValueName): 登録するときのデータの名前(同じ名前を2回以上使うと上書きされる)
            data (JSONType): 登録するデータ
        """
        if cls.initial_regist:
            atexit.register(cls._finalize)
            cls.initial_regist = False
        cls.registed_data[value_name] = data
    
    @classmethod
    def _finalize(cls):
        """外部からの呼び出し禁止
        """
        damped_data = json.dumps(cls.registed_data)
        print(f"# @Recorder: {damped_data}", file=sys.stderr)
    
    @staticmethod
    def get_registed_data(stderr: str|None) -> RegistedData:
        """登録したデータを取得する

        Args:
            stderr (str | None): 標準エラー出力

        Returns:
            RegistedData: registで登録したデータ
        """
        if stderr is None:
            return dict()
        for str in stderr.splitlines()[::-1]:
            # 後ろからチェックして一番最初にマッチした結果だけ返す
            match = re.match(r'# @Recorder: (\{.*\})', str)
            if match:
                registed_data = match.group(1)
                return json.loads(registed_data)
        return dict()
