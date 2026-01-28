import Head from 'next/head'

export default function Home() {
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://job-scraper-o879.onrender.com'

  return (
    <>
      <Head>
        <title>Job Scraper</title>
        <script src="https://unpkg.com/htmx.org@1.9.4"></script>
        <script src="https://unpkg.com/alpinejs@3.12.0" defer></script>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet" />
      </Head>
      <main className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow">
          <h1 className="text-2xl font-semibold mb-4">Job Scraper — フロントエンド</h1>

          <form
            id="scrapeForm"
            className="space-y-4"
            hx-post={`${backendUrl}/run`}
            hx-trigger="submit"
            hx-target="#result"
            hx-swap="innerHTML"
            hx-encoding="multipart/form-data"
            >
            <div>
              <label className="block mb-1">求人ページのURL(例: ATGP / doda)</label>
              <input name="link" type="text" required placeholder="https://..." className="w-full border p-2 rounded" />
            </div>

            <div>
              <label className="block mb-1">実行オプション</label>
              <select name="mode" className="w-full border p-2 rounded">
                <option value="run">実行して CSV/XLSX を作成</option>
              </select>
            </div>

            <div className="flex items-center space-x-2">
              <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">実行</button>
              <span className="text-sm text-gray-500">実行するとバックエンドでスクレイピングが始まり、完了後にダウンロード用リンクが表示されます。</span>
            </div>
          </form>

          <div id="result" className="mt-6"></div>

          <div className="mt-6 text-xs text-gray-500">
            <p>注意: サイトの構造やアクセス制限により取得できない場合があります。大規模な連続リクエストは避けてください。</p>
          </div>
        </div>
      </main>
    </>
  )
}
