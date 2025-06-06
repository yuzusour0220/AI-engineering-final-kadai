import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const markdownPlugins: any[] = [remarkGfm];
import { SubmissionResponse } from '@/types/api';

interface AdviceDisplayProps {
  executionResult: SubmissionResponse | null;
  isLoading?: boolean;
}

/**
 * コード実行結果とアドバイスを表示するコンポーネント
 */
const AdviceDisplay: React.FC<AdviceDisplayProps> = ({ executionResult, isLoading = false }) => {
  if (isLoading) {
    return (
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">実行中...</h3>
        <div className="animate-pulse">
          <div className="h-4 bg-blue-200 rounded w-3/4 mb-2"></div>
          <div className="h-4 bg-blue-200 rounded w-1/2 mb-2"></div>
          <div className="h-4 bg-blue-200 rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  if (!executionResult) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-3">実行結果</h3>
        <div className="text-gray-500">
          コードを実行すると、ここに結果が表示されます
        </div>
      </div>
    );
  }

  const hasError = executionResult.exit_code !== 0 || executionResult.stderr;
  
  return (
    <div className="space-y-4">
      {/* 実行結果 */}
      <div className={`border rounded-lg p-6 ${hasError ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
        <div className="flex items-center justify-between mb-3">
          <h3 className={`text-lg font-semibold ${hasError ? 'text-red-900' : 'text-green-900'}`}>
            実行結果
          </h3>
          <div className="flex items-center space-x-4 text-sm">
            {executionResult.execution_time_ms !== null && (
              <span className={`${hasError ? 'text-red-700' : 'text-green-700'}`}>
                実行時間: {executionResult.execution_time_ms}ms
              </span>
            )}
            {executionResult.exit_code !== null && (
              <span className={`${hasError ? 'text-red-700' : 'text-green-700'}`}>
                終了コード: {executionResult.exit_code}
              </span>
            )}
          </div>
        </div>

        {/* 標準出力 */}
        {executionResult.stdout && (
          <div className="mb-4">
            <h4 className={`font-medium mb-2 ${hasError ? 'text-red-800' : 'text-green-800'}`}>
              標準出力:
            </h4>
            <pre className={`text-sm p-3 rounded border whitespace-pre-wrap ${
              hasError 
                ? 'bg-red-100 border-red-200 text-red-900' 
                : 'bg-green-100 border-green-200 text-green-900'
            }`}>
              {executionResult.stdout}
            </pre>
          </div>
        )}

        {/* 標準エラー */}
        {executionResult.stderr && (
          <div className="mb-4">
            <h4 className="font-medium text-red-800 mb-2">エラー出力:</h4>
            <pre className="text-sm bg-red-100 border border-red-200 text-red-900 p-3 rounded whitespace-pre-wrap">
              {executionResult.stderr}
            </pre>
          </div>
        )}

        {/* メッセージ */}
        {executionResult.message && (
          <div className={`text-sm ${hasError ? 'text-red-700' : 'text-green-700'}`}>
            {executionResult.message}
          </div>
        )}
      </div>

      {/* AIアドバイス */}
      {executionResult.advice_text && (
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6 shadow-sm">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <span className="text-2xl">🤖</span>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-blue-900">AIアドバイス</h3>
              <p className="text-sm text-blue-700">コードの改善提案やヒントです</p>
            </div>
          </div>
          <div className="bg-white rounded-lg p-4 border border-blue-100">
            <ReactMarkdown
              className="prose max-w-none text-gray-800 leading-relaxed"
              remarkPlugins={markdownPlugins}
            >
              {executionResult.advice_text}
            </ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdviceDisplay;
