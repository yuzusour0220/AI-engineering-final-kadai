import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.sandbox_service import execute_python_code_sync, notebook_to_python

# 実際のNotebookファイルを読み込み
with open('深層生成モデル_第1回宿題.ipynb', 'r', encoding='utf-8') as f:
    notebook_content = f.read()

print("Converting notebook to Python code...")
try:
    python_code = notebook_to_python(notebook_content)
    print("Notebook converted successfully!")
    print("First 500 characters of extracted code:")
    print(python_code[:500])
    print("\n" + "="*50)
    
    print("Executing code in Docker...")
    result = execute_python_code_sync(python_code)
    
    print(f"Exit code: {result.exit_code}")
    print(f"Execution time: {result.execution_time_ms:.2f}ms")
    print(f"Succeeded: {result.succeeded}")
    
    if result.stdout:
        print(f"Stdout:\n{result.stdout}")
    
    if result.stderr:
        print(f"Stderr:\n{result.stderr}")
    
    if result.error_type:
        print(f"Error type: {result.error_type}")
        
except Exception as e:
    print(f"Error: {e}")
