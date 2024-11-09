import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import subprocess

import pytest

from recorder import Recorder

def run_and_get_result(command):
    proc = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    ret = Recorder.get_registed_data(proc.stderr)
    # 戻り値がdict型であること
    assert type(ret) is dict
    return ret

def test_recorder_get_normal_data():
    data = run_and_get_result("python tests/subprocess_with_recorder.py")

    from tests.subprocess_with_recorder import test_data

    for key, value in data.items():
        # 型が変化していないこと
        assert type(value) is eval(key)
        # キーがテストデータに含まれること
        assert key in test_data

        test_value = test_data[key]
        # 値が一致すること
        assert value == test_value

def test_recorder_get_no_data():
    data = run_and_get_result("python tests/subprocess_without_recorder.py")

    # データが空であること
    assert data == {}

def test_recorder_raise_error():
    # Recorderはインスタンス化するとTypeErrorする
    with pytest.raises(TypeError):
        _ = Recorder()
