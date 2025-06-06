// API関連の型定義

export interface Problem {
    id: number;
    title: string;
    description: string;
    correct_code: string;
    test_input?: string | null;  // test_inputフィールドを追加
    created_at: string;
    updated_at: string;
}

// 新規作成・更新時に使用する型
export interface ProblemCreate {
    id?: number;
    title: string;
    description: string;
    correct_code: string;
    test_input?: string | null;
}

export interface SubmissionCreate {
    problem_id: number;
    user_code: string;
    code_type?: "python" | "notebook";
}

export interface SubmissionResponse {
    message: string;
    stdout?: string | null;  // 実行標準出力
    stderr?: string | null;  // 実行標準エラー
    execution_time_ms?: number | null;  // 実行時間（ミリ秒）
    exit_code?: number | null;  // 終了コード
    advice_text?: string | null;  // AIからのアドバイス（将来用）
}
