// API関連の型定義

export interface Problem {
    id: number;
    title: string;
    description: string;
    correct_code: string;
    created_at: string;
    updated_at: string;
}

export interface SubmissionCreate {
    problem_id: number;
    user_code: string;
}

export interface SubmissionResponse {
    message: string;
}
