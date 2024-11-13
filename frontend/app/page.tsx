// frontend/app/page.tsx
import { Suspense } from 'react'
import { Metadata } from 'next'
import NovelList from '@/components/NovelList'
import CharacterList from '@/components/CharacterList'
import Loading from '@/components/Common/Loading'
import { fetchNovels, fetchFeaturedCharacters } from '@/lib/api/novels'

// メタデータの定義（SEO対策）
export const metadata: Metadata = {
  title: 'NovelSpec - Your Professional Novel Writing Platform',
  description: 'Organize your novel writing process with advanced tools for plot management, character development, and world building.',
  keywords: 'novel writing, writing tools, plot management, character development, world building',
  openGraph: {
    title: 'NovelSpec - Professional Novel Writing Platform',
    description: 'Advanced tools for novel writing and story development',
    images: ['/images/novelspec-og.jpg'],
  },
}

// メインページコンポーネント
export default async function HomePage() {
  // Server Componentで並列データフェッチ
  const novelsPromise = fetchNovels()
  const charactersPromise = fetchFeaturedCharacters()

  const [novels, featuredCharacters] = await Promise.all([
    novelsPromise,
    charactersPromise,
  ])

  return (
    <main className="min-h-screen px-4 py-8 md:px-6 lg:px-8">
      <section className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          Welcome to NovelSpec
        </h1>
        
        {/* 最近の小説セクション */}
        <div className="mb-12">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">
            Recent Novels
          </h2>
          <Suspense fallback={<Loading />}>
            <NovelList novels={novels} />
          </Suspense>
        </div>

        {/* 注目のキャラクターセクション */}
        <div className="mb-12">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">
            Featured Characters
          </h2>
          <Suspense fallback={<Loading />}>
            <CharacterList characters={featuredCharacters} />
          </Suspense>
        </div>

        {/* 機能紹介セクション */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <FeatureCard
            title="Plot Management"
            description="Organize your story structure and plot points effectively"
            icon="📝"
          />
          <FeatureCard
            title="Character Development"
            description="Create and manage detailed character profiles"
            icon="👤"
          />
          <FeatureCard
            title="World Building"
            description="Build and document your story's universe"
            icon="🌍"
          />
        </section>
      </section>
    </main>
  )
}

// 機能カードコンポーネント
function FeatureCard({
  title,
  description,
  icon,
}: {
  title: string
  description: string
  icon: string
}) {
  return (
    <div className="p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

// エラーバウンダリーコンポーネント
export function ErrorBoundary({ error }: { error: Error }) {
  return (
    <div className="p-4 text-center">
      <h2 className="text-2xl font-bold text-red-600">Something went wrong!</h2>
      <p className="text-gray-600">{error.message}</p>
    </div>
  )
}