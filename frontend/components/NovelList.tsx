'use client';

import { useEffect, useState } from 'react';
import { Box, Grid, Typography, Card, CardContent, Skeleton } from '@mui/material';
import { styled } from '@mui/material/styles';
import { useRouter } from 'next/navigation';
import { fetchNovels } from '../lib/api/novels';

// 型定義
interface Novel {
  id: string;
  title: string;
  description: string;
  author: string;
  updatedAt: string;
  coverImage?: string;
}

// スタイル付きコンポーネント
const NovelCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  cursor: 'pointer',
  transition: 'transform 0.2s ease-in-out',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.shadows[4],
  },
}));

const NovelList = () => {
  const router = useRouter();
  const [novels, setNovels] = useState<Novel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadNovels = async () => {
      try {
        const data = await fetchNovels();
        setNovels(data);
        setLoading(false);
      } catch (err) {
        setError('小説の読み込み中にエラーが発生しました。');
        setLoading(false);
      }
    };

    loadNovels();
  }, []);

  // ローディングスケルトン
  const LoadingSkeleton = () => (
    <Grid container spacing={3}>
      {[...Array(6)].map((_, index) => (
        <Grid item xs={12} sm={6} md={4} key={index}>
          <Skeleton variant="rectangular" height={200} />
        </Grid>
      ))}
    </Grid>
  );

  if (loading) return <LoadingSkeleton />;
  if (error) return <Typography color="error">{error}</Typography>;

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" sx={{ mb: 4 }}>
        小説一覧
      </Typography>
      <Grid container spacing={3}>
        {novels.map((novel) => (
          <Grid item xs={12} sm={6} md={4} key={novel.id}>
            <NovelCard onClick={() => router.push(`/novels/${novel.id}`)}>
              <CardContent>
                {novel.coverImage && (
                  <Box
                    component="img"
                    src={novel.coverImage}
                    alt={novel.title}
                    sx={{
                      width: '100%',
                      height: 200,
                      objectFit: 'cover',
                      mb: 2,
                    }}
                  />
                )}
                <Typography variant="h6" component="h2" gutterBottom>
                  {novel.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  著者: {novel.author}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {novel.description.length > 100
                    ? `${novel.description.substring(0, 100)}...`
                    : novel.description}
                </Typography>
                <Typography variant="caption" color="text.secondary" sx={{ mt: 2 }}>
                  最終更新: {new Date(novel.updatedAt).toLocaleDateString()}
                </Typography>
              </CardContent>
            </NovelCard>
          </Grid>
        ))}
      </Grid>
      {novels.length === 0 && (
        <Typography variant="body1" sx={{ textAlign: 'center', mt: 4 }}>
          小説が見つかりませんでした。
        </Typography>
      )}
    </Box>
  );
};

export default NovelList;