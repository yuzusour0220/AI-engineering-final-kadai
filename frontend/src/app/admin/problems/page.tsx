"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { fetchProblems, deleteProblem, ApiError } from "@/lib/api";
import { Problem } from "@/types/api";

export default function AdminProblemsPage() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const router = useRouter();

  const loadProblems = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchProblems();
      setProblems(data);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("問題の取得に失敗しました");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProblems();
  }, []);

  const handleDelete = async (id: number) => {
    if (!confirm("本当に削除しますか？")) return;
    try {
      setDeletingId(id);
      await deleteProblem(id);
      await loadProblems();
    } catch (err) {
      if (err instanceof ApiError) {
        alert(err.message);
      } else {
        alert("削除に失敗しました");
      }
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">課題一覧</h1>
        <Link
          href="/admin/problems/new"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          新規課題作成
        </Link>
      </div>

      {error && (
        <div className="mb-4 text-red-600">{error}</div>
      )}

      {loading ? (
        <div>読み込み中...</div>
      ) : (
        <table className="min-w-full bg-white border">
          <thead>
            <tr>
              <th className="border px-4 py-2 w-12">ID</th>
              <th className="border px-4 py-2">タイトル</th>
              <th className="border px-4 py-2 w-32">操作</th>
            </tr>
          </thead>
          <tbody>
            {problems.map((p) => (
              <tr key={p.id}>
                <td className="border px-4 py-2 text-center">{p.id}</td>
                <td className="border px-4 py-2">{p.title}</td>
                <td className="border px-4 py-2 text-center space-x-2">
                  <Link
                    href={`/admin/problems/${p.id}/edit`}
                    className="text-blue-600 hover:underline"
                  >
                    編集
                  </Link>
                  <button
                    onClick={() => handleDelete(p.id)}
                    disabled={deletingId === p.id}
                    className="text-red-600 hover:underline"
                  >
                    {deletingId === p.id ? "削除中" : "削除"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
