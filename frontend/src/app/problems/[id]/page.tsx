"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import CodeEditor from "@/components/CodeEditor";
import ExecutionResultDisplay from "@/components/ExecutionResultDisplay";
import { fetchProblem, submitCode, submitCodeFile, ApiError } from "@/lib/api";
import { Problem, SubmissionResponse } from "@/types/api";

export default function ProblemPage() {
  const params = useParams();
  const problemId = params.id as string;

  const [problem, setProblem] = useState<Problem | null>(null);
  const [code, setCode] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [executionResult, setExecutionResult] = useState<SubmissionResponse | null>(null);
  const [showResultArea, setShowResultArea] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] || null;
    setFile(selected);
    if (selected) {
      selected.text().then(setCode);
    } else {
      setCode("");
    }
  };

  // 問題データを取得
  useEffect(() => {
    const loadProblem = async () => {
      try {
        console.log(`Loading problem with ID: ${problemId}`);
        setIsLoading(true);
        setError(null);
        const problemData = await fetchProblem(problemId);
        console.log('Problem data loaded successfully:', problemData);
        setProblem(problemData);
      } catch (err) {
        console.error('Error loading problem:', err);
        if (err instanceof ApiError) {
          console.error('API Error details:', { status: err.status, message: err.message });
          setError(`API Error (${err.status}): ${err.message}`);
        } else {
          console.error('Unknown error:', err);
          setError(`予期しないエラーが発生しました: ${err instanceof Error ? err.message : 'Unknown error'}`);
        }
      } finally {
        setIsLoading(false);
      }
    };

    if (problemId) {
      console.log('Problem ID found:', problemId);
      loadProblem();
    } else {
      console.log('No problem ID found');
      setError('問題IDが指定されていません');
    }
  }, [problemId]);

  // コード提出処理
  const handleSubmit = async () => {
    if (!problem || (!code.trim() && !file)) {
      setError("コードを入力するかファイルを選択してください");
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);
      setExecutionResult(null);
      
      // 実行結果表示エリアを表示
      setShowResultArea(true);

      let response: SubmissionResponse;

      // ファイルがアップロードされている場合はファイル提出API使用
      if (file) {
        response = await submitCodeFile(problem.id, file);
      } else {
        // テキスト入力の場合は通常の提出API使用
        response = await submitCode({
          problem_id: problem.id,
          user_code: code,
          code_type: "python",
        });
      }

      setExecutionResult(response);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("提出に失敗しました");
      }
      setShowResultArea(false);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-lg text-gray-600">問題を読み込み中...</div>
        </div>
      </div>
    );
  }

  if (error && !problem) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-lg font-medium text-red-800 mb-2">エラー</h2>
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-gray-600">問題が見つかりません</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* ナビゲーション */}
      <div className="mb-6">
        <Link
          href="/"
          className="inline-flex items-center text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          ← ホームに戻る
        </Link>
      </div>

      {/* ヘッダー */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {problem.title}
        </h1>
        <div className="text-sm text-gray-500">
          作成日: {new Date(problem.created_at).toLocaleDateString("ja-JP")}
        </div>
      </div>

      {/* 縦並びレイアウト */}
      <div className="space-y-8">
        {/* 問題文セクション */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">問題文</h2>
          <div className="prose prose-gray max-w-none">
            <pre className="whitespace-pre-wrap text-sm bg-gray-50 p-4 rounded border">
              {problem.description}
            </pre>
          </div>
        </div>

        {/* コードエディターセクション */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Pythonコード (.py) または Jupyter Notebook (.ipynb) を入力してください
          </h2>

          <div className="mb-4">
            <input type="file" accept=".py,.ipynb" onChange={handleFileChange} />
            {file && (
              <p className="text-sm text-gray-600 mt-1">{file.name}</p>
            )}
          </div>

          <div className="mb-4">
            <CodeEditor
              value={code}
              onChange={setCode}
              language="python"
              height="400px"
            />
          </div>

          {/* エラー表示 */}
          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 rounded p-3">
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}

          {/* 提出ボタン */}
          <button
            onClick={handleSubmit}
            disabled={isSubmitting || (!code.trim() && !file)}
            className={`w-full py-3 px-4 rounded-lg font-medium transition-colors ${
              isSubmitting || (!code.trim() && !file)
                ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                : "bg-blue-600 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            }`}
          >
            {isSubmitting ? "提出中..." : "コードを提出"}
          </button>
        </div>

        {/* 実行結果・アドバイス表示エリア */}
        {showResultArea && (
          <ExecutionResultDisplay 
            executionResult={executionResult} 
            isLoading={isSubmitting} 
          />
        )}
      </div>
    </div>
  );
}
