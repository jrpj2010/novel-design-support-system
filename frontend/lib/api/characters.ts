import axios from 'axios';

// 環境変数からAPIのベースURLを取得
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// キャラクター型定義
export interface Character {
  id: string;
  name: string;
  description: string;
  age?: number;
  gender?: string;
  role?: string;
  personality?: string[];
  background?: string;
  relationships?: {
    characterId: string;
    relationship: string;
  }[];
  created_at: string;
  updated_at: string;
}

// キャラクター作成用の入力型
export interface CreateCharacterInput {
  name: string;
  description: string;
  age?: number;
  gender?: string;
  role?: string;
  personality?: string[];
  background?: string;
  relationships?: {
    characterId: string;
    relationship: string;
  }[];
}

// キャラクター更新用の入力型
export type UpdateCharacterInput = Partial<CreateCharacterInput>;

// キャラクターAPI関連の関数を含むオブジェクト
export const charactersApi = {
  // 全てのキャラクターを取得
  async getAllCharacters(): Promise<Character[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/characters`);
      return response.data;
    } catch (error) {
      console.error('Error fetching characters:', error);
      throw error;
    }
  },

  // 特定のキャラクターを取得
  async getCharacter(id: string): Promise<Character> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/characters/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching character ${id}:`, error);
      throw error;
    }
  },

  // 新しいキャラクターを作成
  async createCharacter(data: CreateCharacterInput): Promise<Character> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/characters`, data);
      return response.data;
    } catch (error) {
      console.error('Error creating character:', error);
      throw error;
    }
  },

  // キャラクターを更新
  async updateCharacter(id: string, data: UpdateCharacterInput): Promise<Character> {
    try {
      const response = await axios.put(`${API_BASE_URL}/api/characters/${id}`, data);
      return response.data;
    } catch (error) {
      console.error(`Error updating character ${id}:`, error);
      throw error;
    }
  },

  // キャラクターを削除
  async deleteCharacter(id: string): Promise<void> {
    try {
      await axios.delete(`${API_BASE_URL}/api/characters/${id}`);
    } catch (error) {
      console.error(`Error deleting character ${id}:`, error);
      throw error;
    }
  },

  // キャラクター間の関係を設定
  async setCharacterRelationship(
    characterId: string,
    relatedCharacterId: string,
    relationship: string
  ): Promise<void> {
    try {
      await axios.post(`${API_BASE_URL}/api/characters/${characterId}/relationships`, {
        relatedCharacterId,
        relationship,
      });
    } catch (error) {
      console.error('Error setting character relationship:', error);
      throw error;
    }
  },

  // キャラクターの検索
  async searchCharacters(query: string): Promise<Character[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/characters/search`, {
        params: { q: query },
      });
      return response.data;
    } catch (error) {
      console.error('Error searching characters:', error);
      throw error;
    }
  },
};

export default charactersApi;