import { Problem, SubmissionCreate, SubmissionResponse } from "@/types/api";

// サーバーサイドとクライアントサイドで異なるAPI URLを使用
const getApiBaseUrl = () => {
    // サーバーサイドの場合（Node.js環境）
    if (typeof window === 'undefined') {
        return process.env.NEXT_PUBLIC_API_URL_INTERNAL || "http://backend:8000";
    }
    // クライアントサイドの場合（ブラウザ環境）
    return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
};

export class ApiError extends Error {
    constructor(public status: number, message: string) {
        super(message);
        this.name = "ApiError";
    }
}

// 問題詳細を取得
export async function fetchProblem(id: string): Promise<Problem> {
    const apiUrl = getApiBaseUrl();
    console.log(`Fetching problem with ID: ${id} from ${apiUrl}/problems/${id}`);
    console.log(`Running on: ${typeof window === 'undefined' ? 'server-side' : 'client-side'}`);

    try {
        const response = await fetch(`${apiUrl}/problems/${id}`);
        console.log(`Response status: ${response.status}, ok: ${response.ok}`);

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`API Error: ${response.status} - ${errorText}`);

            if (response.status === 404) {
                throw new ApiError(404, "問題が見つかりません");
            }
            throw new ApiError(response.status, `問題の取得に失敗しました: ${errorText}`);
        }

        const data = await response.json();
        console.log('Fetched problem data:', data);
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        if (error instanceof ApiError) {
            throw error;
        }
        if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
            throw new ApiError(500, `ネットワークエラー: APIサーバーに接続できません (${apiUrl})`);
        }
        throw new ApiError(500, `ネットワークエラー: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
}

// コードを提出
export async function submitCode(submission: SubmissionCreate): Promise<SubmissionResponse> {
    const apiUrl = getApiBaseUrl();
    console.log(`Submitting code to ${apiUrl}/submissions/`);

    try {
        const response = await fetch(`${apiUrl}/submissions/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(submission),
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Submit API Error: ${response.status} - ${errorText}`);
            throw new ApiError(response.status, "コードの提出に失敗しました");
        }

        return response.json();
    } catch (error) {
        console.error('Submit error:', error);
        if (error instanceof ApiError) {
            throw error;
        }
        if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
            throw new ApiError(500, `ネットワークエラー: APIサーバーに接続できません (${apiUrl})`);
        }
        throw new ApiError(500, `ネットワークエラー: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
}

// 問題リストを取得
export async function fetchProblems(): Promise<Problem[]> {
    const apiUrl = getApiBaseUrl();
    console.log(`Fetching problems from ${apiUrl}/problems/`);

    try {
        const response = await fetch(`${apiUrl}/problems/`);
        console.log(`Response status: ${response.status}, ok: ${response.ok}`);

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`API Error: ${response.status} - ${errorText}`);
            throw new ApiError(response.status, `問題リストの取得に失敗しました: ${errorText}`);
        }

        const data = await response.json();
        console.log('Fetched problems:', data);
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        if (error instanceof ApiError) {
            throw error;
        }
        if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
            throw new ApiError(500, `ネットワークエラー: APIサーバーに接続できません (${apiUrl})`);
        }
        throw new ApiError(500, `ネットワークエラー: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
}
