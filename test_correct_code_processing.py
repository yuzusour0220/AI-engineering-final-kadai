#!/usr/bin/env python3
"""
課題作成時のファイルアップロード機能をテストするスクリプト
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "backend", "services"))

from sandbox_service import notebook_to_python


def test_jupyter_notebook_processing():
    """Jupyter Notebookファイルの処理をテストする"""

    # サンプルのJupyter Notebookコンテンツ
    sample_notebook = """{
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "print('Hello from notebook!')"
      ]
    },
    {
      "cell_type": "code", 
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "def add(a, b):\\n",
        "    return a + b\\n",
        "\\n",
        "print(add(2, 3))"
      ]
    }
  ],
  "metadata": {},
  "nbformat": 4,
  "nbformat_minor": 4
}"""

    print("=== Jupyter Notebookの処理テスト ===")
    try:
        python_code = notebook_to_python(sample_notebook)
        print("変換されたPythonコード:")
        print(python_code)
        print("\n✅ テスト成功: Jupyter Notebookが正常に処理されました")
    except Exception as e:
        print(f"❌ テスト失敗: {e}")


def test_vscode_notebook_processing():
    """VSCode形式のNotebookファイルの処理をテストする"""

    # サンプルのVSCode形式Notebookコンテンツ
    vscode_notebook = """<VSCode.Cell language="python">
print("Hello from VSCode notebook!")
</VSCode.Cell>

<VSCode.Cell language="python">
def multiply(x, y):
    return x * y

result = multiply(4, 5)
print(f"4 × 5 = {result}")
</VSCode.Cell>"""

    print("\n=== VSCode Notebookの処理テスト ===")
    try:
        python_code = notebook_to_python(vscode_notebook)
        print("変換されたPythonコード:")
        print(python_code)
        print("\n✅ テスト成功: VSCode Notebookが正常に処理されました")
    except Exception as e:
        print(f"❌ テスト失敗: {e}")


if __name__ == "__main__":
    test_jupyter_notebook_processing()
    test_vscode_notebook_processing()
