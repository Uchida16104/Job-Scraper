import Head from 'next/head'
import { useEffect } from 'react'

export default function Home() {
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://job-scraper-gy8f.onrender.com'

  useEffect(() => {
    console.log('Backend URL:', backendUrl)
  }, [backendUrl])

  return (
    <>
      <Head>
        <title>Job Scraper - 求人情報スクレイピングツール</title>
        <meta name="description" content="求人サイトから情報を抽出してCSV/XLSXファイルを生成" />
        <script src="https://unpkg.com/htmx.org@1.9.4"></script>
        <script src="https://unpkg.com/alpinejs@3.12.0" defer></script>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet" />
      </Head>
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
        <div className="max-w-4xl mx-auto">
          {/* ヘッダー */}
          <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">🔍 Job Scraper</h1>
            <p className="text-gray-600">求人サイトから情報を抽出してExcelファイルを生成します</p>
            <div className="mt-4 p-3 bg-blue-50 rounded text-sm text-blue-700">
              <strong>バックエンドURL:</strong> <code className="bg-white px-2 py-1 rounded">{backendUrl}</code>
            </div>
          </div>

          {/* メインフォーム */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <form
              id="scrapeForm"
              className="space-y-6"
              hx-post={`${backendUrl}/run`}
              hx-trigger="submit"
              hx-target="#result"
              hx-swap="innerHTML"
              hx-indicator="#loading"
            >
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  求人ページのURL <span className="text-red-500">*</span>
                </label>
                <input
                  name="link"
                  type="url"
                  required
                  placeholder="https://www.atgp.jp/ など"
                  className="w-full border-2 border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 p-3 rounded-lg transition-all"
                />
                <p className="mt-1 text-xs text-gray-500">例: ATGP, doda, リクナビNEXT などの求人サイト</p>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">実行モード</label>
                <select
                  name="mode"
                  className="w-full border-2 border-gray-300 focus:border-blue-500 p-3 rounded-lg"
                >
                  <option value="run">CSV/XLSX ファイルを生成</option>
                </select>
              </div>

              <div className="flex items-center space-x-4">
                <button
                  type="submit"
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold px-8 py-3 rounded-lg shadow-md transition-all transform hover:scale-105"
                >
                  🚀 実行
                </button>
                <div id="loading" className="htmx-indicator">
                  <div className="flex items-center space-x-2 text-blue-600">
                    <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span className="font-medium">処理中...</span>
                  </div>
                </div>
              </div>
            </form>

            {/* 結果表示エリア */}
            <div id="result" className="mt-6"></div>
          </div>

          {/* 注意事項 */}
          <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <h3 className="font-semibold text-yellow-800 mb-2">⚠️ 注意事項</h3>
            <ul className="text-sm text-yellow-700 space-y-1 list-disc list-inside">
              <li>サイトの構造やアクセス制限により取得できない場合があります</li>
              <li>処理には30秒〜2分程度かかる場合があります</li>
              <li>大規模な連続リクエストは避けてください</li>
              <li>利用は各サイトの利用規約に従ってください</li>
            </ul>
          </div>

          {/* デバッグ情報 */}
          <div className="mt-4 text-center">
            <a
              href={`${backendUrl}/test`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-blue-600 hover:underline"
            >
              🔧 バックエンド接続テスト
            </a>
          </div>
        </div>
      </main>
    </>
  )
}
