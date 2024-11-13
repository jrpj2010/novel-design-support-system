import axios from 'axios';

// 環境変数からAPIのベースURLを取得
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// 世界観の型定義
export interface World {
  id: string;
  name: string;
  description: string;
  rules: string[];
  locations: Location[];
  cultures: Culture[];
  created_at: string;
  updated_at: string;
}

interface Location {
  id: string;
  name: string;
  description: string;
  coordinates?: {
    x: number;
    y: number;
  };
}

interface Culture {
  id: string;
  name: string;
  description: string;
  customs: string[];
}

// APIエラーの型定義
interface ApiError {
  message: string;
  status: number;
}

// 世界観の作成
export async function createWorld(worldData: Omit<World, 'id' | 'created_at' | 'updated_at'>): Promise<World> {
  try {
    const response = await axios.post<World>(`${API_BASE_URL}/api/worldbuilding`, worldData);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
}

// 世界観の取得
export async function getWorld(worldId: string): Promise<World> {
  try {
    const response = await axios.get<World>(`${API_BASE_URL}/api/worldbuilding/${worldId}`);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
}

// 全世界観のリスト取得
export async function listWorlds(): Promise<World[]> {
  try {
    const response = await axios.get<World[]>(`${API_BASE_URL}/api/worldbuilding`);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
}

// 世界観の更新
export async function updateWorld(worldId: string, worldData: Partial<World>): Promise<World> {
  try {
    const response = await axios.put<World>(`${API_BASE_URL}/api/worldbuilding/${worldId}`, worldData);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
}

// 世界観の削除
export async function deleteWorld(worldId: string): Promise<void> {
  try {
    await axios.delete(`${API_BASE_URL}/api/worldbuilding/${worldId}`);
  } catch (error) {
    throw handleApiError(error);
  }
}

// ロケーションの追加
export async function addLocation(worldId: string, location: Omit<Location, 'id'>): Promise<Location> {
  try {
    const response = await axios.post<Location>(
      `${API_BASE_URL}/api/worldbuilding/${worldId}/locations`,
      location
    );
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
}

// 文化の追加
export async function addCulture(worldId: string, culture: Omit<Culture, 'id'>): Promise<Culture> {
  try {
    const response = await axios.post<Culture>(
      `${API_BASE_URL}/api/worldbuilding/${worldId}/cultures`,
      culture
    );
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
}

// エラーハンドリングヘルパー関数
function handleApiError(error: any): ApiError {
  if (axios.isAxiosError(error)) {
    return {
      message: error.response?.data?.message || 'An error occurred while communicating with the server',
      status: error.response?.status || 500,
    };
  }
  return {
    message: 'An unexpected error occurred',
    status: 500,
  };
}