import axios from 'axios';
import { API_BASE_URL } from '../config';

// 小説に関する型定義
export interface Novel {
  id: string;
  title: string;
  description: string;
  created_at: string;
  updated_at: string;
  author_id: string;
}

export interface Chapter {
  id: string;
  novel_id: string;
  title: string;
  content: string;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface NovelMetadata {
  genre: string[];
  tags: string[];
  status: 'draft' | 'published' | 'archived';
  target_audience: string;
  language: string;
}

// APIクライアントの設定
const api = axios.create({
  baseURL: `${API_BASE_URL}/api/novels`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 小説関連のAPI関数
export const novelsApi = {
  // 小説一覧の取得
  async getAllNovels() {
    const response = await api.get<Novel[]>('/');
    return response.data;
  },

  // 特定の小説の取得
  async getNovel(id: string) {
    const response = await api.get<Novel>(`/${id}`);
    return response.data;
  },

  // 新規小説の作成
  async createNovel(novelData: Omit<Novel, 'id' | 'created_at' | 'updated_at'>) {
    const response = await api.post<Novel>('/', novelData);
    return response.data;
  },

  // 小説の更新
  async updateNovel(id: string, novelData: Partial<Novel>) {
    const response = await api.put<Novel>(`/${id}`, novelData);
    return response.data;
  },

  // 小説の削除
  async deleteNovel(id: string) {
    await api.delete(`/${id}`);
  },

  // チャプター関連の操作
  chapters: {
    // チャプター一覧の取得
    async getChapters(novelId: string) {
      const response = await api.get<Chapter[]>(`/${novelId}/chapters`);
      return response.data;
    },

    // 特定のチャプターの取得
    async getChapter(novelId: string, chapterId: string) {
      const response = await api.get<Chapter>(`/${novelId}/chapters/${chapterId}`);
      return response.data;
    },

    // チャプターの作成
    async createChapter(novelId: string, chapterData: Omit<Chapter, 'id' | 'created_at' | 'updated_at'>) {
      const response = await api.post<Chapter>(`/${novelId}/chapters`, chapterData);
      return response.data;
    },

    // チャプターの更新
    async updateChapter(novelId: string, chapterId: string, chapterData: Partial<Chapter>) {
      const response = await api.put<Chapter>(`/${novelId}/chapters/${chapterId}`, chapterData);
      return response.data;
    },

    // チャプターの削除
    async deleteChapter(novelId: string, chapterId: string) {
      await api.delete(`/${novelId}/chapters/${chapterId}`);
    },
  },

  // メタデータ関連の操作
  metadata: {
    // メタデータの取得
    async getMetadata(novelId: string) {
      const response = await api.get<NovelMetadata>(`/${novelId}/metadata`);
      return response.data;
    },

    // メタデータの更新
    async updateMetadata(novelId: string, metadata: Partial<NovelMetadata>) {
      const response = await api.put<NovelMetadata>(`/${novelId}/metadata`, metadata);
      return response.data;
    },
  },
};

// エラーハンドリングのためのカスタムエラークラス
export class NovelApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public originalError: any
  ) {
    super(message);
    this.name = 'NovelApiError';
  }
}

// API呼び出しのエラーハンドリングラッパー
export async function handleApiRequest<T>(request: Promise<T>): Promise<T> {
  try {
    return await request;
  } catch (error: any) {
    if (axios.isAxiosError(error)) {
      throw new NovelApiError(
        error.response?.data?.message || 'API request failed',
        error.response?.status || 500,
        error
      );
    }
    throw error;
  }
}