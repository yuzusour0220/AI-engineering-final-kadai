import React from 'react';

interface AdviceDisplayProps {
  advice: string | null;
  isLoading?: boolean;
}

/**
 * コード提出後のアドバイスを表示するコンポーネント
 */
const AdviceDisplay: React.FC<AdviceDisplayProps> = ({ advice, isLoading = false }) => {
  // アドバイスの内容がない場合のデフォルトメッセージ
  const defaultMessage = 'ここにアドバイスが表示されます';
  
  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
      <h3 className="text-lg font-semibold text-blue-900 mb-3">アドバイス</h3>
      
      {isLoading ? (
        <div className="animate-pulse">
          <div className="h-4 bg-blue-200 rounded w-3/4 mb-2"></div>
          <div className="h-4 bg-blue-200 rounded w-1/2 mb-2"></div>
          <div className="h-4 bg-blue-200 rounded w-2/3"></div>
        </div>
      ) : (
        <div className="text-blue-800 whitespace-pre-wrap">
          {advice || defaultMessage}
        </div>
      )}
    </div>
  );
};

export default AdviceDisplay;
