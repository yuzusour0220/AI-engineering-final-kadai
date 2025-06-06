import json
import sys
import os

# servicesへのパスを追加
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from services.sandbox_service import notebook_to_python


def test_notebook_to_python():
    """標準的なJupyter Notebookのテスト"""
    nb = {
        "cells": [
            {
                "cell_type": "code",
                "source": "a = 1\nb = 2\nprint(a + b)",
                "metadata": {},
                "execution_count": 1,
            },
            {"cell_type": "markdown", "source": "# Title", "metadata": {}},
            {
                "cell_type": "code",
                "source": "print('done')",
                "metadata": {},
                "execution_count": 2,
            },
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 2,
    }
    nb_str = json.dumps(nb)
    code = notebook_to_python(nb_str)
    assert "a = 1" in code
    assert "print('done')" in code


def test_notebook_with_null_execution_count():
    """execution_countがnullのJupyter Notebookのテスト"""
    nb = {
        "cells": [
            {
                "cell_type": "code",
                "source": "x = 5\nprint(x)",
                "metadata": {},
                "execution_count": None,
            },
            {"cell_type": "markdown", "source": "# Test", "metadata": {}},
            {
                "cell_type": "code",
                "source": "y = 10\nprint(y)",
                "metadata": {},
                "execution_count": None,
            },
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 2,
    }
    nb_str = json.dumps(nb)
    code = notebook_to_python(nb_str)
    assert "x = 5" in code
    assert "y = 10" in code


def test_vscode_notebook():
    """VSCode形式のnotebookのテスト"""
    vscode_nb = """
    <VSCode.Cell id="test1" language="python">
import numpy as np
print("Hello VSCode")
    </VSCode.Cell>
    <VSCode.Cell id="test2" language="markdown">
# This is markdown
    </VSCode.Cell>
    <VSCode.Cell id="test3" language="python">
result = 42
print(result)
    </VSCode.Cell>
    """
    code = notebook_to_python(vscode_nb)
    assert "import numpy as np" in code
    assert "result = 42" in code
    assert "# This is markdown" not in code


if __name__ == "__main__":
    test_notebook_to_python()
    test_notebook_with_null_execution_count()
    test_vscode_notebook()
    print("All tests passed!")
