"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { fetchProblems, ApiError } from "@/lib/api";
import { Problem } from "@/types/api";

export default function Home() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadProblems = async () => {
      try {
        console.log('Loading problems...');
        setIsLoading(true);
        setError(null);
        const problemsData = await fetchProblems();
        console.log('Problems loaded successfully:', problemsData);
        setProblems(problemsData);
      } catch (err) {
        console.error('Error loading problems:', err);
        if (err instanceof ApiError) {
          setError(`API Error (${err.status}): ${err.message}`);
        } else {
          setError(`予期しないエラーが発生しました: ${err instanceof Error ? err.message : 'Unknown error'}`);
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadProblems();
  }, []);

  const getBorderColor = (index: number) => {
    const colors = ["border-blue-500", "border-green-500", "border-purple-500", "border-red-500", "border-yellow-500"];
    return colors[index % colors.length];
  };

  const getTextColor = (index: number) => {
    const colors = ["text-blue-500", "text-green-500", "text-purple-500", "text-red-500", "text-yellow-500"];
    return colors[index % colors.length];
  };

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

        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-lg text-gray-600">問題を読み込み中...</div>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-2xl mx-auto">
            <h2 className="text-lg font-medium text-red-800 mb-2">エラー</h2>
            <p className="text-red-600">{error}</p>
          </div>
        ) : problems.length === 0 ? (
          <div className="text-center text-gray-600">問題が見つかりません</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl mx-auto">
            {problems.map((problem, index) => (
              <Link
                key={problem.id}
                href={`/problems/${problem.id}`}
                className={`bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow border-l-4 ${getBorderColor(index)}`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900 mb-2">
                      問題 {problem.id}: {problem.title}
                    </h2>
                    <p className="text-gray-600 text-sm">
                      {problem.description.length > 50 
                        ? `${problem.description.substring(0, 50)}...` 
                        : problem.description}
                    </p>
                  </div>
                  <div className={`${getTextColor(index)} text-2xl`}>→</div>
                </div>
              </Link>
            ))}
          </div>
        )}

        <div className="mt-12 bg-white rounded-lg shadow-md p-8 max-w-2xl mx-auto">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4 text-center">
            システムの使い方
          </h2>
          <div className="space-y-4 text-gray-600">
            <div className="flex items-start space-x-3">
              <div className="bg-blue-100 text-blue-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold">
                1
              </div>
              <div>
                <h3 className="font-medium text-gray-900">問題を選択</h3>
                <p className="text-sm">上から解きたい問題をクリックしてください</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="bg-green-100 text-green-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold">
                2
              </div>
              <div>
                <h3 className="font-medium text-gray-900">コードを記述</h3>
                <p className="text-sm">右側のエディターにPythonコードを入力</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="bg-purple-100 text-purple-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold">
                3
              </div>
              <div>
                <h3 className="font-medium text-gray-900">コードを提出</h3>
                <p className="text-sm">「コードを提出」ボタンで実行結果を確認</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="bg-red-100 text-red-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold">
                4
              </div>
              <div>
                <h3 className="font-medium text-gray-900">結果を確認</h3>
                <p className="text-sm">実行結果やエラーメッセージをチェック（将来的にはAIアドバイスも追加予定）</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
