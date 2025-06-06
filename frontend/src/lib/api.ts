import { Problem, ProblemCreate, SubmissionCreate, SubmissionResponse } from "@/types/api";

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

export async function submitCodeFile(problemId: number, file: File): Promise<SubmissionResponse> {
    const apiUrl = getApiBaseUrl();
    console.log(`Submitting code file to ${apiUrl}/submissions/upload`);

    const formData = new FormData();
    formData.append("problem_id", String(problemId));
    formData.append("file", file);

    // ファイル拡張子に基づいてcode_typeを設定
    const codeType = file.name.endsWith(".ipynb") ? "notebook" : "python";
    formData.append("code_type", codeType);

    try {
        const response = await fetch(`${apiUrl}/submissions/upload`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Submit File API Error: ${response.status} - ${errorText}`);
            throw new ApiError(response.status, "コードファイルの提出に失敗しました");
        }

        return response.json();
    } catch (error) {
        console.error('Submit file error:', error);
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

// 新しい問題を作成
export async function createProblem(problem: ProblemCreate): Promise<Problem> {
    const apiUrl = getApiBaseUrl();
    try {
        const response = await fetch(`${apiUrl}/problems/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(problem),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new ApiError(response.status, `問題の作成に失敗しました: ${errorText}`);
        }
        return response.json();
    } catch (error) {
        if (error instanceof ApiError) {
            throw error;
        }
        throw new ApiError(500, `ネットワークエラー: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
}

// 既存の問題を更新
export async function updateProblem(id: number, problem: ProblemCreate): Promise<Problem> {
    const apiUrl = getApiBaseUrl();
    try {
        const response = await fetch(`${apiUrl}/problems/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(problem),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new ApiError(response.status, `問題の更新に失敗しました: ${errorText}`);
        }
        return response.json();
    } catch (error) {
        if (error instanceof ApiError) {
            throw error;
        }
        throw new ApiError(500, `ネットワークエラー: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
}

// 問題を削除
export async function deleteProblem(id: number): Promise<void> {
    const apiUrl = getApiBaseUrl();
    try {
        const response = await fetch(`${apiUrl}/problems/${id}`, {
            method: "DELETE",
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new ApiError(response.status, `問題の削除に失敗しました: ${errorText}`);
        }
    } catch (error) {
        if (error instanceof ApiError) {
            throw error;
        }
        throw new ApiError(500, `ネットワークエラー: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
}
