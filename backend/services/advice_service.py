# AIアドバイス生成サービス
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from .sandbox_service import notebook_to_python
import logging

logger = logging.getLogger(__name__)

load_dotenv()
# 使用するモデル名
HUGGINGFACE_MODEL_ID = "Qwen/Qwen2.5-72B-Instruct"
# Hugging Face InferenceClient を初期化
client = InferenceClient(
    provider="nebius",  # または "huggingface" など適切なプロバイダーを指定
    token=os.getenv("HUGGINGFACE_API_KEY"),
)


async def generate_advice_with_huggingface(
    problem_title: str,
    problem_description: str,
    user_code: str,
    execution_stdout: str | None,
    execution_stderr: str | None,
    correct_code: str | None = None,
    is_correct: bool = False,
) -> str:
    """指定された情報を基にHugging Faceのモデルからアドバイスを生成する"""

    # 正解コードがnotebook形式の場合、Pythonコードに変換
    processed_correct_code = None
    if correct_code:
        try:
            # JSONかXML形式かを判定してnotebook処理を試す
            if correct_code.strip().startswith(("{", "<")):
                processed_correct_code = notebook_to_python(correct_code)
            else:
                processed_correct_code = correct_code
        except Exception:
            # notebook処理に失敗した場合は元のコードを使用
            processed_correct_code = correct_code

    prompt_string = f"""
【判定結果】
{"正解です！素晴らしい！" if is_correct else "不正解です。"}

あなたは、Pythonプログラミングを学ぶ初学者をサポートする親切なAIアシスタントです。
以下の情報に基づいて、学習者が自分で間違いに気づき、解決できるようになるためのヒントやアドバイスを生成してください。

【重要】
- **絶対にコードの正解そのものを直接教えてはいけません。**
- 指摘は具体的かつ建設的に行い、学習者のモチベーションを維持するよう努めてください。
- 難しい専門用語は避け、分かりやすい言葉で説明してください。
- アドバイスは日本語でお願いします。
{"- 正解の場合は、コードの改善点や別の解き方などを提案してください。" if is_correct else ""}

【課題情報】
タイトル: {problem_title}
問題文:
{problem_description}

【学習者の提出コード】
```python
{user_code}
```

【コードの実行結果】
標準出力:
{execution_stdout if execution_stdout else "なし"}
標準エラー:
{execution_stderr if execution_stderr else "なし"}

【アドバイスのポイント】
1.  **エラーがある場合:**
    - エラーメッセージ ({execution_stderr}) が何を意味するのか、考えられる原因は何かを優しく説明してください。
    - エラーが発生している箇所を特定するためのデバッグ方法（例: print文の挿入箇所など）を提案してください。
2.  **エラーがないが期待通りに動作しない場合 (または改善点がある場合):**
    - コードのロジックで改善できる点や、より効率的な書き方があれば示唆してください。
    - 変数名やコメントの付け方など、読みやすいコードにするための一般的なアドバイスも適宜含めてください。
    - (もし正解コードが提供されていれば、それを直接見せるのではなく、学習者のコードとの違いからヒントを得られるような問いかけをしてください)
3.  **よくある間違いの指摘:**
    - 初学者が陥りやすい間違いのパターンに合致する場合は、それとなく教えてあげてください。
      (例: for文の範囲、インデックスエラー、無限ループの可能性など)

"""

    # 正解コードがある場合はプロンプトに追加
    if processed_correct_code:
        prompt_string += f"""【参考：正解コード】
```python
{processed_correct_code}
```

"""

    prompt_string += "上記を踏まえて、学習者へのアドバイスを生成してください。"

    try:
        completion = client.chat.completions.create(
            model=HUGGINGFACE_MODEL_ID,
            messages=[{"role": "user", "content": prompt_string}],
            max_tokens=1500,
        )
        advice_text = completion.choices[0].message.content
        return advice_text
    except Exception as e:
        logger.error("Hugging Face API呼び出し中にエラーが発生しました: %s", e)
        return "申し訳ありません。アドバイスの生成中にエラーが発生しました。"
