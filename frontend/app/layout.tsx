// frontend/app/layout.tsx
import { Metadata } from 'next'
import { Suspense } from 'react'
import { Inter } from 'next/font/google'
import { NovelContextProvider } from '@/contexts/NovelContext'
import Layout from '@/components/Layout'
import Loading from '@/components/Common/Loading'
import '@/styles/globals.css'

// フォントの設定
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

// メタデータの設定
export const metadata: Metadata = {
  title: {
    default: 'NovelSpec - Novel Writing Management Tool',
    template: '%s | NovelSpec',
  },
  description: 'Professional novel writing and management platform for authors',
  keywords: ['novel writing', 'author tools', 'writing management', 'story planning'],
  authors: [{ name: 'NovelSpec Team' }],
  creator: 'NovelSpec',
  publisher: 'NovelSpec',
  robots: {
    index: true,
    follow: true,
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://novelspec.com',
    siteName: 'NovelSpec',
    title: 'NovelSpec - Novel Writing Management Tool',
    description: 'Professional novel writing and management platform for authors',
    images: [
      {
        url: '/images/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'NovelSpec',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'NovelSpec - Novel Writing Management Tool',
    description: 'Professional novel writing and management platform for authors',
    images: ['/images/twitter-image.jpg'],
  },
}

interface RootLayoutProps {
  children: React.ReactNode
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" className={inter.variable}>
      <body>
        <NovelContextProvider>
          <Suspense fallback={<Loading />}>
            <Layout>
              {children}
            </Layout>
          </Suspense>
        </NovelContextProvider>
      </body>
    </html>
  )
}

// レスポンシブデザインとアクセシビリティのための追加スタイル設定
export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: '#ffffff',
}

// セキュリティヘッダーの設定
export const headers = {
  'Content-Security-Policy': `
    default-src 'self';
    script-src 'self' 'unsafe-eval' 'unsafe-inline';
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    font-src 'self' https://fonts.gstatic.com;
    img-src 'self' data: https:;
    connect-src 'self' ${process.env.NEXT_PUBLIC_API_URL};
  `,
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
}

// キャッシュの設定
export const revalidate = 3600 // 1時間ごとに再検証