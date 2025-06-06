import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { SubmissionResponse } from '@/types/api';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const markdownPlugins: any[] = [remarkGfm];

interface ExecutionResultDisplayProps {
  executionResult: SubmissionResponse | null;
  isLoading?: boolean;
}

/**
 * コード実行結果を詳細に表示するコンポーネント
 */
const ExecutionResultDisplay: React.FC<ExecutionResultDisplayProps> = ({ 
  executionResult, 
  isLoading = false 
}) => {
  if (isLoading) {
    return (
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <div className="flex items-center space-x-3 mb-4">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
          <h3 className="text-lg font-semibold text-blue-900">実行中...</h3>
        </div>
        <div className="animate-pulse space-y-2">
          <div className="h-4 bg-blue-200 rounded w-3/4"></div>
          <div className="h-4 bg-blue-200 rounded w-1/2"></div>
          <div className="h-4 bg-blue-200 rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  if (!executionResult) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
        <div className="flex items-center space-x-3 mb-3">
          <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-500">
            ⏳
          </div>
          <h3 className="text-lg font-semibold text-gray-700">実行結果</h3>
        </div>
        <div className="text-gray-500">
          コードを実行すると、ここに結果が表示されます
        </div>
      </div>
    );
  }

  const hasError = executionResult.exit_code !== 0 || (executionResult.stderr && executionResult.stderr.trim() !== '');
  const isSuccess = !hasError;

  return (
    <div className="space-y-4">
      {/* メイン実行結果 */}
      <div className={`border rounded-lg p-6 ${
        hasError 
          ? 'bg-red-50 border-red-200' 
          : 'bg-green-50 border-green-200'
      }`}>
        {/* ヘッダー */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className={`flex items-center justify-center w-10 h-10 rounded-full text-lg font-bold ${
              hasError 
                ? 'bg-red-100 text-red-600' 
                : 'bg-green-100 text-green-600'
            }`}>
              {hasError ? '✗' : '✓'}
            </div>
            <div>
              <h3 className={`text-xl font-semibold ${
                hasError ? 'text-red-900' : 'text-green-900'
              }`}>
                実行結果
              </h3>
              <p className={`text-sm ${
                hasError ? 'text-red-700' : 'text-green-700'
              }`}>
                {hasError ? 'エラーが発生しました' : '正常に実行されました'}
              </p>
            </div>
          </div>
          
          {/* 実行統計 */}
          <div className="text-right space-y-1">
            {executionResult.execution_time_ms !== null && executionResult.execution_time_ms !== undefined && (
              <div className={`text-sm font-medium ${
                hasError ? 'text-red-700' : 'text-green-700'
              }`}>
                ⏱️ {Math.round(executionResult.execution_time_ms)}ms
              </div>
            )}
            {executionResult.exit_code !== null && (
              <div className={`text-xs px-2 py-1 rounded ${
                hasError 
                  ? 'bg-red-200 text-red-800' 
                  : 'bg-green-200 text-green-800'
              }`}>
                終了コード: {executionResult.exit_code}
              </div>
            )}
          </div>
        </div>

        {/* 標準出力 */}
        {executionResult.stdout && executionResult.stdout.trim() && (
          <div className="mb-4">
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-lg">📄</span>
              <h4 className={`font-medium ${
                hasError ? 'text-red-800' : 'text-green-800'
              }`}>
                出力結果:
              </h4>
            </div>
            <div className={`relative ${
              hasError 
                ? 'bg-red-100 border-red-200' 
                : 'bg-green-100 border-green-200'
            } border rounded-lg`}>
              <pre className={`text-sm p-4 whitespace-pre-wrap overflow-x-auto ${
                hasError ? 'text-red-900' : 'text-green-900'
              }`}>
                {executionResult.stdout}
              </pre>
              <div className={`absolute top-2 right-2 text-xs px-2 py-1 rounded ${
                hasError 
                  ? 'bg-red-200 text-red-700' 
                  : 'bg-green-200 text-green-700'
              }`}>
                stdout
              </div>
            </div>
          </div>
        )}

        {/* 標準エラー */}
        {executionResult.stderr && executionResult.stderr.trim() && (
          <div className="mb-4">
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-lg">⚠️</span>
              <h4 className="font-medium text-red-800">エラー出力:</h4>
            </div>
            <div className="bg-red-100 border border-red-200 rounded-lg relative">
              <pre className="text-sm text-red-900 p-4 whitespace-pre-wrap overflow-x-auto">
                {executionResult.stderr}
              </pre>
              <div className="absolute top-2 right-2 text-xs bg-red-200 text-red-700 px-2 py-1 rounded">
                stderr
              </div>
            </div>
          </div>
        )}

        {/* システムメッセージ */}
        {executionResult.message && (
          <div className={`text-sm p-3 rounded-lg ${
            hasError 
              ? 'bg-red-100 text-red-700 border border-red-200' 
              : 'bg-green-100 text-green-700 border border-green-200'
          }`}>
            <div className="flex items-center space-x-2">
              <span>{hasError ? '🔍' : 'ℹ️'}</span>
              <span className="font-medium">システムメッセージ:</span>
            </div>
            <div className="mt-1">{executionResult.message}</div>
          </div>
        )}

        {/* 成功時の追加情報 */}
        {isSuccess && !executionResult.stdout && (
          <div className="bg-green-100 border border-green-200 rounded-lg p-3">
            <div className="flex items-center space-x-2 text-green-700">
              <span>✨</span>
              <span className="text-sm">
                コードは正常に実行されましたが、出力はありませんでした。
              </span>
            </div>
          </div>
        )}
      </div>

      {/* AIアドバイス（将来実装予定） */}
      {executionResult.advice_text && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="flex items-center space-x-3 mb-3">
            <span className="text-2xl">🤖</span>
            <h3 className="text-lg font-semibold text-blue-900">AIアドバイス</h3>
          </div>
          <ReactMarkdown
            className="prose max-w-none text-blue-800"
            remarkPlugins={markdownPlugins}
          >
            {executionResult.advice_text}
          </ReactMarkdown>
        </div>
      )}

      {/* エラー時のヘルプメッセージ */}
      {hasError && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <span className="text-lg">💡</span>
            <h4 className="font-medium text-yellow-800">デバッグのヒント:</h4>
          </div>
          <ul className="text-sm text-yellow-700 space-y-1 ml-6">
            <li>• エラーメッセージを注意深く読んでください</li>
            <li>• 行番号があればその行を確認してください</li>
            <li>• インデント（空白）が正しいか確認してください</li>
            <li>• 変数名のスペルミスがないか確認してください</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default ExecutionResultDisplay;
