# Job Scraper - クイックスタートガイド

## 🚀 最速セットアップ (5分で起動)

### ローカル環境で今すぐ起動

```bash
# 1. プロジェクトディレクトリに移動
cd job-scraper

# 2. バックエンドを起動 (ターミナル1)
cd backend
./start-local.sh

# 3. フロントエンドを起動 (ターミナル2 - 新しいウィンドウを開く)
cd frontend
./start-local.sh

# 4. ブラウザでアクセス
# http://localhost:3000
```

これだけ!すぐに使えます。

---

## 📝 Render & Vercel デプロイ (10分で完了)

### Step 1: Renderでバックエンドをデプロイ

1. [Render](https://render.com) にGitHubでログイン
2. **New Web Service** をクリック
3. リポジトリ `job-scraper` を選択
4. 設定:
   - **Root Directory**: `backend`
   - **Runtime**: `Docker`
   - **Region**: `Singapore`
5. 環境変数を追加:
   ```
   APP_NAME=JobScraper
   APP_ENV=production
   APP_KEY=base64:ランダムな文字列
   APP_DEBUG=false
   APP_URL=https://あなたのアプリ.onrender.com
   FRONTEND_URL=https://あなたのアプリ.vercel.app
   SESSION_DRIVER=file
   FILESYSTEM_DISK=public
   ```
6. **Create Web Service** をクリック

**APP_KEYの取得方法:**
```bash
cd backend
php artisan key:generate --show
# 出力をコピーしてRenderの環境変数に貼り付け
```

### Step 2: Vercelでフロントエンドをデプロイ

1. [Vercel](https://vercel.com) にGitHubでログイン
2. **Add New Project** をクリック
3. リポジトリ `job-scraper` を選択
4. 設定:
   - **Framework**: `Next.js`
   - **Root Directory**: `frontend`
5. 環境変数を追加:
   ```
   NEXT_PUBLIC_BACKEND_URL=https://あなたのRenderアプリ.onrender.com
   ```
6. **Deploy** をクリック

### Step 3: URLを相互に設定

1. VercelのURLをコピー
2. Renderの環境変数 `FRONTEND_URL` に設定
3. RenderのURLをコピー
4. Vercelの環境変数 `NEXT_PUBLIC_BACKEND_URL` に設定

完了!これで世界中からアクセスできます。

---

## 🎯 使い方

1. フロントエンドのURLにアクセス
2. 求人サイトのURL を入力 (例: `https://www.atgp.jp/`)
3. **実行** をクリック
4. 30秒〜2分待つ
5. CSV/XLSXファイルのダウンロードリンクが表示
6. クリックしてダウンロード

---

## 📂 プロジェクト構成

```
job-scraper/
├── backend/          # Laravel + Python バックエンド
│   ├── app/          # Laravelアプリケーション
│   ├── main.py       # Pythonスクレイピングスクリプト
│   ├── Dockerfile    # Render用Dockerファイル
│   └── start-local.sh  # ローカル起動スクリプト
│
├── frontend/         # Next.js フロントエンド
│   ├── pages/        # Reactページ
│   ├── package.json
│   └── start-local.sh  # ローカル起動スクリプト
│
├── DEPLOY.md         # 詳細なデプロイ手順
└── README.md         # このファイル
```

---

## 🛠️ トラブルシューティング

### ローカルで動かない

```bash
# 権限エラーの場合
chmod +x backend/start-local.sh frontend/start-local.sh

# Pythonエラーの場合
pip3 install -r backend/requirements.txt --break-system-packages
```

### デプロイで動かない

1. **Renderのログを確認**
   - Dashboard → Logs タブ
2. **環境変数を確認**
   - APP_KEY が設定されているか
   - URL が正しいか
3. **DEPLOY.md を参照**

---

## 📚 詳細なドキュメント

- [DEPLOY.md](./DEPLOY.md) - 完全デプロイガイド
- [backend/README.md](./backend/README.md) - バックエンド詳細
- [frontend/README.md](./frontend/README.md) - フロントエンド詳細

---

## ✅ チェックリスト

### ローカル開発

- [ ] PHP 8.1+ インストール済み
- [ ] Composer インストール済み
- [ ] Node.js 18+ インストール済み
- [ ] Python 3.9+ インストール済み
- [ ] Google Chrome インストール済み
- [ ] バックエンドが http://localhost:8000 で起動
- [ ] フロントエンドが http://localhost:3000 で起動
- [ ] スクレイピングが正常に動作

### デプロイ

- [ ] GitHubリポジトリ作成済み
- [ ] Renderでバックエンドデプロイ完了
- [ ] Vercelでフロントエンドデプロイ完了
- [ ] 環境変数が正しく設定されている
- [ ] 本番環境でスクレイピングが動作

---

**これで完璧です! 🎉**

問題があれば DEPLOY.md のトラブルシューティングを確認してください。
