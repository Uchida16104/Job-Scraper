import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Script from 'next/script';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: '求人スクレイピングシステム / Job Scraping System',
  description: '複数の求人サイトから情報を一括収集 / Collect information from multiple job sites',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <head>
        <Script src="https://unpkg.com/htmx.org@latest" strategy="beforeInteractive" />
        <Script src="https://unpkg.com/alpinejs@latest" strategy="beforeInteractive" defer />
      </head>
      <body className={inter.className}>
        <nav className="bg-primary-600 text-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <a href="/" className="text-xl font-bold">
                  求人スクレイピングシステム / Job Scraper
                </a>
              </div>
              <div className="flex items-center space-x-4">
                <a
                  href="/"
                  className="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-700 transition-colors"
                >
                  検索 / Search
                </a>
                <a
                  href="/history"
                  className="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-700 transition-colors"
                >
                  履歴 / History
                </a>
              </div>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="bg-gray-100 mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <p className="text-center text-gray-600 text-sm">
              © 2024 Job Scraper System. All rights reserved.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
