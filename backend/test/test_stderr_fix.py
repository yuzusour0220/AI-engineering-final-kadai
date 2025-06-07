#!/usr/bin/env python3
"""
stderr変数の修正をテストするスクリプト
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.sandbox_service import execute_python_code_sync, notebook_to_python

def test_stderr_fix():
    """stderr変数修正のテスト"""
    
    # テスト1: 基本的なコード実行
    print("Test 1: Basic code execution")
    code = """
import numpy as np
import pandas as pd
print("Basic test successful")
"""
    result = execute_python_code_sync(code)
    print(f"Exit code: {result.exit_code}")
    print(f"Stdout: {result.stdout}")
    print(f"Stderr: {result.stderr}")
    print(f"Succeeded: {result.succeeded}")
    print("-" * 50)
    
    # テスト2: pipインストールを含むコード
    print("Test 2: Code with pip install")
    code_with_pip = """
!pip install requests
import requests
print("Pip install test successful")
"""
    result = execute_python_code_sync(code_with_pip)
    print(f"Exit code: {result.exit_code}")
    print(f"Stdout: {result.stdout}")
    print(f"Stderr: {result.stderr}")
    print(f"Succeeded: {result.succeeded}")
    print("-" * 50)
    
    # テスト3: エラーが発生するコード
    print("Test 3: Code with error")
    error_code = """
print("Before error")
undefined_variable
print("After error")
"""
    result = execute_python_code_sync(error_code)
    print(f"Exit code: {result.exit_code}")
    print(f"Stdout: {result.stdout}")
    print(f"Stderr: {result.stderr}")
    print(f"Succeeded: {result.succeeded}")
    print("-" * 50)

if __name__ == "__main__":
    test_stderr_fix()
