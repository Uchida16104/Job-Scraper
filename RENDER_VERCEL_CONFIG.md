# Render & Vercel 設定サマリー

## ⚙️ Render (バックエンド) 設定

### 基本設定

| 項目 | 設定値 |
|------|--------|
| Service Type | Web Service |
| Name | `job-scraper-backend` (任意) |
| Region | **Singapore (Southeast Asia)** 推奨 |
| Branch | `main` |
| Root Directory | **`backend`** |
| Runtime | **`Docker`** |
| Dockerfile Path | **`backend/Dockerfile`** |

### 環境変数 (Environment Variables)

```plaintext
APP_NAME=JobScraper
APP_ENV=production
APP_KEY=base64:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
APP_DEBUG=false
APP_URL=https://your-app-name.onrender.com
LOG_CHANNEL=stack
LOG_LEVEL=info
FRONTEND_URL=https://your-app-name.vercel.app
SESSION_DRIVER=file
SESSION_LIFETIME=120
FILESYSTEM_DISK=public
```

**重要:** 
- `APP_KEY` はローカルで `php artisan key:generate --show` で生成
- `APP_URL` はRenderから割り当てられたURLに後で更新
- `FRONTEND_URL` はVercelから割り当てられたURLに後で更新

### デプロイ設定

- **Auto-Deploy**: `Yes` (Git pushで自動デプロイ)
- **Branch**: `main`
- **Build Command**: Dockerfileに記載 (自動実行)
- **Start Command**: Dockerfileに記載 (Apache起動)

---

## ⚙️ Vercel (フロントエンド) 設定

### プロジェクト設定

| 項目 | 設定値 |
|------|--------|
| Framework Preset | **Next.js** |
| Root Directory | **`frontend`** |
| Build Command | `npm run build` (デフォルト) |
| Output Directory | `.next` (デフォルト) |
| Install Command | `npm install` (デフォルト) |
| Node.js Version | 18.x (デフォルト) |

### 環境変数 (Environment Variables)

```plaintext
NEXT_PUBLIC_BACKEND_URL=https://your-backend-app.onrender.com
```

**重要:** 
- `NEXT_PUBLIC_BACKEND_URL` はRenderから割り当てられたバックエンドのURLに設定
- 環境変数は `NEXT_PUBLIC_` で始める必要があります (Next.jsの仕様)

### デプロイ設定

- **Production Branch**: `main`
- **Auto-Deploy**: `Enabled` (Git pushで自動デプロイ)
- **Install Command**: `npm install` (自動)
- **Build Command**: `npm run build` (自動)

---

## 🔄 デプロイの流れ

### 初回デプロイ

1. **GitHubリポジトリ作成 & プッシュ**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/username/job-scraper.git
   git push -u origin main
   ```

2. **Renderでバックエンドをデプロイ**
   - Web Service作成
   - 環境変数設定 (仮のURLを使用)
   - デプロイ開始 (5〜10分)
   - 割り当てられたURLをメモ

3. **Vercelでフロントエンドをデプロイ**
   - Project作成
   - 環境変数にRenderのURLを設定
   - デプロイ開始 (2〜3分)
   - 割り当てられたURLをメモ

4. **URLを相互に更新**
   - RenderのFRONTEND_URLをVercelのURLに更新
   - RenderのAPP_URLを自身のURLに更新
   - 再デプロイ (自動)

### 更新デプロイ

```bash
# コード変更後
git add .
git commit -m "Update: 変更内容"
git push origin main

# → Render & Vercel で自動デプロイ開始
```

---

## 🔍 デプロイ後のチェックポイント

### Render (バックエンド)

- [ ] ステータスが **Live** になっている
- [ ] ログにエラーがない
- [ ] `https://your-app.onrender.com/` にアクセスして応答がある
- [ ] 環境変数が正しく設定されている
- [ ] `storage/app/public/downloads/` が作成されている

### Vercel (フロントエンド)

- [ ] デプロイが **Ready** になっている
- [ ] ビルドログにエラーがない
- [ ] `https://your-app.vercel.app/` にアクセスしてページが表示される
- [ ] 環境変数 `NEXT_PUBLIC_BACKEND_URL` が正しい
- [ ] フォームが正常に動作する

### 連携テスト

- [ ] フロントエンドからバックエンドに接続できる
- [ ] URLを入力して実行できる
- [ ] スクレイピングが正常に完了する
- [ ] ファイルがダウンロードできる
- [ ] CORSエラーが発生しない

---

## 📊 想定される動作時間

| 処理 | 時間 |
|------|------|
| Renderの初回デプロイ | 5〜10分 |
| Vercelの初回デプロイ | 2〜3分 |
| コード変更後の再デプロイ | 3〜5分 |
| スクレイピング実行時間 | 30秒〜2分 |
| ファイルダウンロード | 即座 |

---

## 🚨 よくあるエラーと対処法

### Renderでのエラー

#### "Build failed"
- Dockerfileの構文エラー確認
- requirements.txtの依存関係確認
- ログで具体的なエラーメッセージを確認

#### "APP_KEY not set"
- 環境変数にAPP_KEYが設定されているか確認
- `base64:` で始まっているか確認

#### "Permission denied" (storage)
- Dockerfileで `chmod -R 775 storage` が実行されているか確認

### Vercelでのエラー

#### "Build failed"
- package.jsonの依存関係確認
- Node.jsバージョンが18以上か確認
- ビルドログで具体的なエラーを確認

#### "Cannot connect to backend"
- 環境変数 `NEXT_PUBLIC_BACKEND_URL` が正しいか確認
- Renderのバックエンドが起動しているか確認
- CORSの設定を確認 (config/cors.php)

---

## 📝 環境変数のテンプレート

### Render用 .env (参考)

```bash
APP_NAME=JobScraper
APP_ENV=production
APP_KEY=base64:生成した長い文字列をここに貼り付け
APP_DEBUG=false
APP_URL=https://job-scraper-backend-xxxxx.onrender.com
LOG_CHANNEL=stack
LOG_LEVEL=info
FRONTEND_URL=https://job-scraper-frontend-xxxxx.vercel.app
SESSION_DRIVER=file
SESSION_LIFETIME=120
FILESYSTEM_DISK=public
```

### Vercel用 .env (参考)

```bash
NEXT_PUBLIC_BACKEND_URL=https://job-scraper-backend-xxxxx.onrender.com
```

---

## 🎯 デプロイ完了の確認方法

1. **ブラウザで両方のURLにアクセス**
   - Render: `https://your-backend.onrender.com/` → JSONレスポンス
   - Vercel: `https://your-frontend.vercel.app/` → フォーム画面

2. **統合テスト実行**
   - フロントエンドで求人サイトのURLを入力
   - 実行ボタンをクリック
   - ダウンロードリンクが表示されるまで待機
   - ファイルをダウンロードして内容確認

3. **成功!** 🎉

---

このガイドに従えば、**エラーなく確実にデプロイできます。**
