'use client';

import { useEffect, useState } from 'react';
import { Box, Grid, Card, CardContent, Typography, Skeleton } from '@mui/material';
import { getCharacters } from '@/lib/api/characters';
import { styled } from '@mui/material/styles';
import { useMediaQuery } from '@mui/material';
import { Character } from '@/types/character';

// スタイル付きコンポーネントの定義
const CharacterCard = styled(Card)(({ theme }) => ({
  height: '100%',
  transition: 'transform 0.2s ease-in-out',
  cursor: 'pointer',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.shadows[4],
  },
}));

const CharacterImage = styled('img')({
  width: '100%',
  height: '200px',
  objectFit: 'cover',
});

interface CharacterListProps {
  initialCharacters?: Character[];
}

export default function CharacterList({ initialCharacters }: CharacterListProps) {
  const [characters, setCharacters] = useState<Character[]>(initialCharacters || []);
  const [loading, setLoading] = useState(!initialCharacters);
  const [error, setError] = useState<string | null>(null);
  
  const isMobile = useMediaQuery('(max-width:600px)');
  const isTablet = useMediaQuery('(max-width:960px)');

  useEffect(() => {
    if (!initialCharacters) {
      fetchCharacters();
    }
  }, [initialCharacters]);

  const fetchCharacters = async () => {
    try {
      setLoading(true);
      const data = await getCharacters();
      setCharacters(data);
    } catch (err) {
      setError('キャラクター情報の取得に失敗しました');
      console.error('Error fetching characters:', err);
    } finally {
      setLoading(false);
    }
  };

  // ローディングスケルトン
  if (loading) {
    return (
      <Grid container spacing={3} padding={2}>
        {[...Array(6)].map((_, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Skeleton variant="rectangular" height={200} />
            <Skeleton variant="text" sx={{ mt: 1 }} />
            <Skeleton variant="text" width="60%" />
          </Grid>
        ))}
      </Grid>
    );
  }

  // エラー表示
  if (error) {
    return (
      <Box p={3}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  // グリッドサイズの動的設定
  const getGridSize = () => {
    if (isMobile) return 12;
    if (isTablet) return 6;
    return 4;
  };

  return (
    <Box component="section" aria-label="キャラクター一覧">
      <Grid container spacing={3} padding={2}>
        {characters.map((character) => (
          <Grid item xs={getGridSize()} key={character.id}>
            <CharacterCard>
              <CharacterImage
                src={character.imageUrl || '/images/character-placeholder.png'}
                alt={`${character.name}の画像`}
                loading="lazy"
              />
              <CardContent>
                <Typography variant="h6" component="h2" gutterBottom>
                  {character.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {character.role}
                </Typography>
                <Typography variant="body2" noWrap>
                  {character.description}
                </Typography>
              </CardContent>
            </CharacterCard>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

// Character型の定義（types/character.tsに移動することを推奨）
interface Character {
  id: string;
  name: string;
  role: string;
  description: string;
  imageUrl?: string;
}
// pages/characters/index.tsx
import CharacterList from '@/components/CharacterList';

export default function CharactersPage() {
  return (
    <div>
      <h1>キャラクター一覧</h1>
      <CharacterList />
    </div>
  );
}