import sys

# サービスパスを追加
sys.path.append(
    "/Users/takumisakai/自主勉/AIエンジニアリング/AI-engineering-final-kadai/backend"
)
from services.sandbox_service import notebook_to_python, execute_python_code_sync

# 実際のnotebookファイルを読み込んでテスト
notebook_path = "/Users/takumisakai/自主勉/AIエンジニアリング/AI-engineering-final-kadai/test_assignment_notebook.ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    content = f.read()

print("=== Notebook Content (first 500 chars) ===")
print(content[:500])
print("\n=== Extracting Python Code ===")

try:
    python_code = notebook_to_python(content)
    print("Successfully extracted Python code:")
    print(python_code)

    print("\n=== Executing Code ===")
    result = execute_python_code_sync(python_code)

    print(f"Exit Code: {result.exit_code}")
    print(f"Succeeded: {result.succeeded}")
    print(f"Stdout: {result.stdout}")
    print(f"Stderr: {result.stderr}")

except Exception as e:
    print(f"Error: {e}")
