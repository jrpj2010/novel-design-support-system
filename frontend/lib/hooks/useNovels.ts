import useSWR, { mutate } from 'swr';
import { useState } from 'react';
import { fetchNovels, createNovel, updateNovel, deleteNovel } from '../api/novels';

export interface Novel {
  id: string;
  title: string;
  description: string;
  author: string;
  created_at: string;
  updated_at: string;
  status: 'draft' | 'published' | 'archived';
  genre?: string;
  wordCount?: number;
}

interface UseNovelsReturn {
  novels: Novel[] | undefined;
  isLoading: boolean;
  error: Error | null;
  createNewNovel: (novelData: Omit<Novel, 'id' | 'created_at' | 'updated_at'>) => Promise<Novel>;
  updateExistingNovel: (id: string, novelData: Partial<Novel>) => Promise<Novel>;
  deleteExistingNovel: (id: string) => Promise<void>;
  refreshNovels: () => Promise<void>;
}

export const useNovels = (): UseNovelsReturn => {
  const [error, setError] = useState<Error | null>(null);

  // SWRを使用してデータをフェッチ
  const { data: novels, error: fetchError, isLoading } = useSWR<Novel[]>(
    '/api/novels',
    fetchNovels
  );

  // 新規小説の作成
  const createNewNovel = async (
    novelData: Omit<Novel, 'id' | 'created_at' | 'updated_at'>
  ): Promise<Novel> => {
    try {
      const newNovel = await createNovel(novelData);
      await mutate('/api/novels'); // キャッシュの更新
      return newNovel;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to create novel'));
      throw err;
    }
  };

  // 既存小説の更新
  const updateExistingNovel = async (
    id: string,
    novelData: Partial<Novel>
  ): Promise<Novel> => {
    try {
      const updatedNovel = await updateNovel(id, novelData);
      await mutate('/api/novels'); // キャッシュの更新
      return updatedNovel;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to update novel'));
      throw err;
    }
  };

  // 小説の削除
  const deleteExistingNovel = async (id: string): Promise<void> => {
    try {
      await deleteNovel(id);
      await mutate('/api/novels'); // キャッシュの更新
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to delete novel'));
      throw err;
    }
  };

  // 手動でデータを再取得
  const refreshNovels = async (): Promise<void> => {
    try {
      await mutate('/api/novels');
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to refresh novels'));
      throw err;
    }
  };

  return {
    novels,
    isLoading,
    error: error || fetchError,
    createNewNovel,
    updateExistingNovel,
    deleteExistingNovel,
    refreshNovels,
  };
};

export default useNovels;