import Head from "next/head";
export default function Home() {
  return (
    <html lang="ja">
      <Head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width,initial-scale=1" />
        <title>Job Scraper</title>
        <script src="https://unpkg.com/htmx.org@1.10.0"></script>
        <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
      </Head>
      <body className="bg-gray-50 min-h-screen">
        <main className="max-w-4xl mx-auto p-6">
          <h1 className="text-3xl font-semibold mb-4">Job Scraper</h1>
          <p className="mb-4">スクレイピングしたい求人一覧のURLを1行ずつ入力してください。各URLごとにCSV/XLSXを生成し、ダウンロードリンクを返します。</p>
          <form id="scrape-form" hx-post="https://YOUR_RENDER_BACKEND_URL/api/scrape" hx-encoding="multipart/form-data" hx-target="#result" hx-swap="innerHTML" className="space-y-4">
            <label className="block">
              <textarea name="urls" rows="6" className="w-full p-3 border rounded" placeholder="https://example.com/job1\nhttps://example.com/job2"></textarea>
            </label>
            <label className="block">
              <input type="text" name="site" className="w-full p-3 border rounded" placeholder="optional: atgp,litalico,mlg,doda,indeed,mynavi,rikunabi or leave empty" />
            </label>
            <div className="flex space-x-2">
              <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">スクレイプ開始</button>
              <button type="button" onclick="document.querySelector('textarea[name=urls]').value='';document.querySelector('input[name=site]').value='';" className="px-4 py-2 bg-gray-200 rounded">クリア</button>
            </div>
          </form>
          <section id="result" className="mt-6"></section>
          <div className="mt-8 text-sm text-gray-600">注意: バックエンドのURL (https://YOUR_RENDER_BACKEND_URL) を Render にデプロイしたバックエンドのURLに置換してください。</div>
        </main>
      </body>
    </html>
  );
}

