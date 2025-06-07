# サンプル正解コード（Pythonファイル）
# FizzBuzz問題の解答例


def fizzbuzz(n):
    """
    1からnまでの数字について、
    3の倍数の場合は"Fizz"、
    5の倍数の場合は"Buzz"、
    15の倍数の場合は"FizzBuzz"、
    それ以外は数字をそのまま出力する
    """
    for i in range(1, n + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


# テスト実行
if __name__ == "__main__":
    fizzbuzz(15)
