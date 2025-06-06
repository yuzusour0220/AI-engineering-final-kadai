"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import CodeEditor from "@/components/CodeEditor";
import { createProblem, ApiError } from "@/lib/api";
import { ProblemCreate } from "@/types/api";

export default function NewProblemPage() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [correctCode, setCorrectCode] = useState("");
  const [testInput, setTestInput] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !description.trim() || !correctCode.trim()) {
      setError("必須項目を入力してください");
      return;
    }
    const payload: ProblemCreate = {
      title,
      description,
      correct_code: correctCode,
      test_input: testInput || null,
    };
    try {
      setSubmitting(true);
      await createProblem(payload);
      router.push("/admin/problems");
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("登録に失敗しました");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="container mx-auto max-w-2xl p-4">
      <h1 className="text-2xl font-bold mb-4">新規課題作成</h1>
      {error && <div className="mb-4 text-red-600">{error}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-medium mb-1">タイトル</label>
          <input
            type="text"
            className="w-full border rounded p-2"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>
        <div>
          <label className="block font-medium mb-1">問題文</label>
          <textarea
            className="w-full border rounded p-2"
            rows={6}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <div>
          <label className="block font-medium mb-1">正解コード</label>
          <CodeEditor value={correctCode} onChange={setCorrectCode} language="python" height="200px" />
        </div>
        <div>
          <label className="block font-medium mb-1">テストケース入力 (省略可)</label>
          <textarea
            className="w-full border rounded p-2"
            rows={2}
            value={testInput}
            onChange={(e) => setTestInput(e.target.value)}
          />
        </div>
        <button
          type="submit"
          disabled={submitting}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          {submitting ? "登録中..." : "登録"}
        </button>
      </form>
    </div>
  );
}
