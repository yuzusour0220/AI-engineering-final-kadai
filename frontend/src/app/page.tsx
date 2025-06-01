import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            プログラミング課題システム
          </h1>
          <p className="text-lg text-gray-600">
            Pythonプログラミングの課題を解いて、スキルアップしましょう！
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl mx-auto">
          <Link
            href="/problems/1"
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow border-l-4 border-blue-500"
          >
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  問題 1: Hello World
                </h2>
                <p className="text-gray-600 text-sm">
                  基本的なPythonプログラムを作成する問題です
                </p>
              </div>
              <div className="text-blue-500 text-2xl">→</div>
            </div>
          </Link>

          <Link
            href="/problems/2"
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow border-l-4 border-green-500"
          >
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  問題 2: 数値の計算
                </h2>
                <p className="text-gray-600 text-sm">
                  変数と計算を使った基本的なプログラム
                </p>
              </div>
              <div className="text-green-500 text-2xl">→</div>
            </div>
          </Link>
        </div>

        <div className="text-center mt-12">
          <div className="bg-white rounded-lg shadow-md p-6 max-w-lg mx-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              使い方
            </h3>
            <ul className="text-sm text-gray-600 space-y-2 text-left">
              <li>• 問題を選択して課題の詳細を確認</li>
              <li>• コードエディターでPythonコードを入力</li>
              <li>• 「コードを提出」ボタンでコードを送信</li>
              <li>• AIからのアドバイスを確認して改善</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
