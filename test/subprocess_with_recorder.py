"""テスト用
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from recorder import Recorder

test_data = [
    ("bool", True),
    ("int", 1),
    ("float", 1.23),
    ("str", "test"),
    ("list", [1, 2, 3]),
    ("dict", {1: 2, 3: 4}),
]

if __name__ == "__main__":
    print("hello.")
    print("hello.", file=sys.stderr)
    for name, data in test_data:
        Recorder.regist(name, data)
    print("test", file=sys.stderr)
