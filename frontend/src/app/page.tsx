"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { fetchProblems, ApiError } from "@/lib/api";
import { Problem } from "@/types/api";

export default function Home() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [filteredProblems, setFilteredProblems] = useState<Problem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [viewMode, setViewMode] = useState<"grid" | "list">("list");

  useEffect(() => {
    const loadProblems = async () => {
      try {
        console.log('Loading problems...');
        setIsLoading(true);
        setError(null);
        const problemsData = await fetchProblems();
        console.log('Problems loaded successfully:', problemsData);
        setProblems(problemsData);
        setFilteredProblems(problemsData);
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

  // 検索機能
  useEffect(() => {
    const filtered = problems.filter(problem => 
      problem.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      problem.description.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredProblems(filtered);
  }, [searchTerm, problems]);

  const getDifficultyBadge = (index: number) => {
    const difficulties = [
      { label: "初級", color: "bg-green-100 text-green-800" },
      { label: "中級", color: "bg-yellow-100 text-yellow-800" },
      { label: "上級", color: "bg-red-100 text-red-800" },
    ];
    return difficulties[index % difficulties.length];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("ja-JP", {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  // リスト表示のコンポーネント
  const ProblemListView = () => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                課題
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                難易度
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                作成日
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                アクション
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredProblems.map((problem, index) => {
              const difficulty = getDifficultyBadge(index);
              return (
                <tr key={problem.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex flex-col">
                      <div className="text-sm font-medium text-gray-900">
                        {problem.title}
                      </div>
                      <div className="text-sm text-gray-500 mt-1 line-clamp-2">
                        {problem.description.length > 100 
                          ? `${problem.description.substring(0, 100)}...` 
                          : problem.description}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${difficulty.color}`}>
                      {difficulty.label}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatDate(problem.created_at)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <Link
                      href={`/problems/${problem.id}`}
                      className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                    >
                      解く
                      <svg className="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </Link>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );

  // グリッド表示のコンポーネント
  const ProblemGridView = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {filteredProblems.map((problem, index) => {
        const difficulty = getDifficultyBadge(index);
        return (
          <Link
            key={problem.id}
            href={`/problems/${problem.id}`}
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-blue-300 transition-all duration-200 group"
          >
            <div className="flex justify-between items-start mb-3">
              <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${difficulty.color}`}>
                {difficulty.label}
              </span>
              <svg className="w-5 h-5 text-gray-400 group-hover:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
              {problem.title}
            </h3>
            <p className="text-gray-600 text-sm mb-3 line-clamp-3">
              {problem.description.length > 120 
                ? `${problem.description.substring(0, 120)}...` 
                : problem.description}
            </p>
            <div className="text-xs text-gray-500 mt-auto">
              作成日: {formatDate(problem.created_at)}
            </div>
          </Link>
        );
      })}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-7xl">
        {/* ヘッダー */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            プログラミング課題システム
          </h1>
          <p className="text-lg text-gray-600">
            Pythonプログラミングの課題を解いて、スキルアップしましょう！
          </p>
        </div>

        {/* コントロール */}
        <div className="mb-6 flex flex-col sm:flex-row gap-4 items-center justify-between">
          <div className="flex-1 max-w-md">
            <div className="relative">
              <input
                type="text"
                placeholder="課題を検索..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <svg className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-600">表示:</span>
            <button
              onClick={() => setViewMode("list")}
              className={`p-2 rounded-md transition-colors ${
                viewMode === "list" 
                  ? "bg-blue-100 text-blue-600" 
                  : "text-gray-400 hover:text-gray-600"
              }`}
              title="リスト表示"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
            </button>
            <button
              onClick={() => setViewMode("grid")}
              className={`p-2 rounded-md transition-colors ${
                viewMode === "grid" 
                  ? "bg-blue-100 text-blue-600" 
                  : "text-gray-400 hover:text-gray-600"
              }`}
              title="グリッド表示"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
            </button>
          </div>
        </div>

        {/* メインコンテンツ */}
        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <div className="text-lg text-gray-600">問題を読み込み中...</div>
            </div>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-2xl mx-auto">
            <h2 className="text-lg font-medium text-red-800 mb-2">エラー</h2>
            <p className="text-red-600">{error}</p>
          </div>
        ) : filteredProblems.length === 0 ? (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.47.726-6.23 1.962A9.964 9.964 0 002 12C2 6.477 6.477 2 12 2s10 4.477 10 10c0 1.81-.481 3.506-1.322 4.97M15 17h5l-5 5v-5z" />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {searchTerm ? "検索結果が見つかりません" : "問題が見つかりません"}
            </h3>
            <p className="text-gray-600">
              {searchTerm ? "別のキーワードで検索してみてください" : "課題が登録されていません"}
            </p>
            {searchTerm && (
              <button
                onClick={() => setSearchTerm("")}
                className="mt-4 text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                検索をクリア
              </button>
            )}
          </div>
        ) : (
          <div className="mb-8">
            {/* 統計情報 */}
            <div className="mb-6 text-sm text-gray-600">
              {searchTerm ? (
                <span>"{searchTerm}" の検索結果: {filteredProblems.length}件</span>
              ) : (
                <span>全 {problems.length} 課題</span>
              )}
            </div>
            
            {/* 課題一覧 */}
            {viewMode === "list" ? <ProblemListView /> : <ProblemGridView />}
          </div>
        )}

        {/* 使い方ガイド（課題がある場合のみ表示） */}
        {!isLoading && !error && problems.length > 0 && (
          <div className="mt-12 bg-white rounded-lg shadow-sm border border-gray-200 p-8 max-w-4xl mx-auto">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6 text-center">
              システムの使い方
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="bg-blue-100 text-blue-600 rounded-full w-12 h-12 flex items-center justify-center text-lg font-bold mx-auto mb-3">
                  1
                </div>
                <h3 className="font-medium text-gray-900 mb-2">問題を選択</h3>
                <p className="text-sm text-gray-600">一覧から解きたい問題をクリック</p>
              </div>
              <div className="text-center">
                <div className="bg-green-100 text-green-600 rounded-full w-12 h-12 flex items-center justify-center text-lg font-bold mx-auto mb-3">
                  2
                </div>
                <h3 className="font-medium text-gray-900 mb-2">コードを記述</h3>
                <p className="text-sm text-gray-600">エディターにPythonコードを入力</p>
              </div>
              <div className="text-center">
                <div className="bg-purple-100 text-purple-600 rounded-full w-12 h-12 flex items-center justify-center text-lg font-bold mx-auto mb-3">
                  3
                </div>
                <h3 className="font-medium text-gray-900 mb-2">コードを提出</h3>
                <p className="text-sm text-gray-600">提出ボタンで実行結果を確認</p>
              </div>
              <div className="text-center">
                <div className="bg-orange-100 text-orange-600 rounded-full w-12 h-12 flex items-center justify-center text-lg font-bold mx-auto mb-3">
                  4
                </div>
                <h3 className="font-medium text-gray-900 mb-2">結果を確認</h3>
                <p className="text-sm text-gray-600">実行結果とAIアドバイスをチェック</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
