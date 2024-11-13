import useSWR, { mutate } from 'swr';
import { Character, CharacterCreate, CharacterUpdate } from '../types/character';
import { 
  getCharacters, 
  getCharacter, 
  createCharacter, 
  updateCharacter, 
  deleteCharacter 
} from '../api/characters';

interface UseCharactersReturn {
  characters: Character[];
  character: Character | null;
  isLoading: boolean;
  isError: any;
  createNewCharacter: (data: CharacterCreate) => Promise<Character>;
  updateExistingCharacter: (id: string, data: CharacterUpdate) => Promise<Character>;
  removeCharacter: (id: string) => Promise<void>;
  getCharacterById: (id: string) => Promise<Character>;
}

/**
 * キャラクター管理のためのカスタムフック
 * @param novelId - 小説ID（オプショナル）
 * @returns キャラクター関連の操作とデータを提供するオブジェクト
 */
export const useCharacters = (novelId?: string): UseCharactersReturn => {
  const { data: characters, error, mutate: mutateCharacters } = useSWR<Character[]>(
    novelId ? `/api/novels/${novelId}/characters` : null,
    () => getCharacters(novelId)
  );

  /**
   * 新しいキャラクターを作成
   */
  const createNewCharacter = async (data: CharacterCreate): Promise<Character> => {
    try {
      const newCharacter = await createCharacter(data, novelId);
      await mutateCharacters([...(characters || []), newCharacter], false);
      return newCharacter;
    } catch (error) {
      console.error('Error creating character:', error);
      throw error;
    }
  };

  /**
   * 既存のキャラクターを更新
   */
  const updateExistingCharacter = async (id: string, data: CharacterUpdate): Promise<Character> => {
    try {
      const updatedCharacter = await updateCharacter(id, data);
      await mutateCharacters(
        characters?.map(char => char.id === id ? updatedCharacter : char),
        false
      );
      return updatedCharacter;
    } catch (error) {
      console.error('Error updating character:', error);
      throw error;
    }
  };

  /**
   * キャラクターを削除
   */
  const removeCharacter = async (id: string): Promise<void> => {
    try {
      await deleteCharacter(id);
      await mutateCharacters(
        characters?.filter(char => char.id !== id),
        false
      );
    } catch (error) {
      console.error('Error deleting character:', error);
      throw error;
    }
  };

  /**
   * IDによるキャラクター取得
   */
  const getCharacterById = async (id: string): Promise<Character> => {
    try {
      const character = await getCharacter(id);
      return character;
    } catch (error) {
      console.error('Error fetching character:', error);
      throw error;
    }
  };

  return {
    characters: characters || [],
    character: null,
    isLoading: !error && !characters,
    isError: error,
    createNewCharacter,
    updateExistingCharacter,
    removeCharacter,
    getCharacterById,
  };
};

export default useCharacters;