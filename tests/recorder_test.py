import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import subprocess

import pytest

from recorder import Recorder

def get_data(strderr):
    ret = Recorder.get_registed_data(strderr)
    # 戻り値がdict型であること
    assert type(ret) is dict
    return ret

def test_recorder_get_normal_data():
    cmd = f"python tests/subprocess_with_recorder.py"
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    data = get_data(proc.stderr)

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
    cmd = f"python tests/subprocess_without_recorder.py"
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    data = get_data(proc.stderr)

    # データが空であること
    assert data == {}

def test_recorder_raise_error():
    # Recorderはインスタンス化するとTypeErrorする
    with pytest.raises(TypeError):
        _ = Recorder()
