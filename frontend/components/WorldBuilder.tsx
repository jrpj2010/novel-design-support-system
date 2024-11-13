'use client';

import React, { useState, useEffect } from 'react';
import { Box, Typography, TextField, Paper, Grid, Button } from '@mui/material';
import { createWorld, updateWorld, getWorld } from '@/lib/api/worlds';
import { useRouter } from 'next/router';
import { MarkdownEditor } from '@/components/Common/MarkdownEditor';
import { FileUploader } from '@/components/Common/FileUploader';
import { Loading } from '@/components/Common/Loading';

interface WorldBuilderProps {
  worldId?: string;
  initialData?: WorldData;
}

interface WorldData {
  id?: string;
  name: string;
  description: string;
  rules: string;
  geography: string;
  culture: string;
  history: string;
  technology: string;
  magic_system: string;
  maps: string[];
}

const WorldBuilder: React.FC<WorldBuilderProps> = ({ worldId, initialData }) => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [worldData, setWorldData] = useState<WorldData>({
    name: '',
    description: '',
    rules: '',
    geography: '',
    culture: '',
    history: '',
    technology: '',
    magic_system: '',
    maps: [],
    ...initialData,
  });

  useEffect(() => {
    const fetchWorld = async () => {
      if (worldId) {
        setLoading(true);
        try {
          const data = await getWorld(worldId);
          setWorldData(data);
        } catch (error) {
          console.error('Error fetching world data:', error);
        }
        setLoading(false);
      }
    };

    if (worldId && !initialData) {
      fetchWorld();
    }
  }, [worldId, initialData]);

  const handleChange = (field: keyof WorldData) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setWorldData((prev) => ({
      ...prev,
      [field]: event.target.value,
    }));
  };

  const handleMarkdownChange = (field: keyof WorldData) => (value: string) => {
    setWorldData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleMapUpload = (files: string[]) => {
    setWorldData((prev) => ({
      ...prev,
      maps: [...prev.maps, ...files],
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (worldId) {
        await updateWorld(worldId, worldData);
      } else {
        const newWorld = await createWorld(worldData);
        router.push(`/world-building/${newWorld.id}`);
      }
    } catch (error) {
      console.error('Error saving world data:', error);
    }
    setLoading(false);
  };

  if (loading) {
    return <Loading />;
  }

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ p: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom>
            {worldId ? 'Edit World' : 'Create New World'}
          </Typography>
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="World Name"
            value={worldData.name}
            onChange={handleChange('name')}
            required
          />
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Description
            </Typography>
            <MarkdownEditor
              value={worldData.description}
              onChange={handleMarkdownChange('description')}
            />
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Rules & Physics
            </Typography>
            <MarkdownEditor
              value={worldData.rules}
              onChange={handleMarkdownChange('rules')}
            />
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Geography
            </Typography>
            <MarkdownEditor
              value={worldData.geography}
              onChange={handleMarkdownChange('geography')}
            />
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Culture
            </Typography>
            <MarkdownEditor
              value={worldData.culture}
              onChange={handleMarkdownChange('culture')}
            />
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Maps
            </Typography>
            <FileUploader
              acceptedTypes={['image/*']}
              onUpload={handleMapUpload}
              multiple
            />
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
            <Button
              variant="outlined"
              onClick={() => router.back()}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="contained"
              color="primary"
            >
              {worldId ? 'Update World' : 'Create World'}
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default WorldBuilder;